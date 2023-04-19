#!/usr/bin/env python3

import cv2
import numpy as np
from gabriel_protocol import gabriel_pb2
from gabriel_client.websocket_client import ProducerWrapper
import logging
import zmq
import openmidas_pb2
import uuid

logger = logging.getLogger(__name__)

class ZmqAdapter:
    def __init__(self, preprocess, source_name, display_frames):
        '''
        preprocess should take one frame parameter
        produce_engine_fields takes no parameters
        consume_frame should take one frame parameter and one engine_fields
        parameter
        '''
        self.location = {}
        self.model = 'DPT_Hybrid'
        self.colormap = cv2.COLORMAP_OCEAN
        self._preprocess = preprocess
        self._source_name = source_name
        self.display_frames = display_frames
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://localhost:5555')
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.frames_processed = 0
        logger.info(f"ZmqAdapter has subscribed to all topics on localhost...")

    def recv_array(self, flags=0, copy=True, track=False):
        """recv a numpy array"""
        md = self.socket.recv_json(flags=flags)
        msg = self.socket.recv(flags=flags, copy=copy, track=track)
        buf = memoryview(msg)
        A = np.frombuffer(buf, dtype=md['dtype'])
        self.model = md['model']
        return A.reshape(md['shape'])

    def produce_extras(self):
        extras = openmidas_pb2.Extras()
        extras.model = self.model
        extras.colormap = self.colormap
        logger.debug(f"Model: {self.model} Colormap: {self.colormap}")
        logger.debug(f"Lat: {self.location['latitude']} Lon: {self.location['longitude']}")
        return extras

    def get_producer_wrappers(self):
        async def producer():
            frame = self.recv_array()

            if frame is None:
                return None

            frame = self._preprocess(frame)
            if self.display_frames:
                cv2.imshow("Frames sent to ZmqAdapter", frame)
                cv2.waitKey(1)

            _, jpeg_frame = cv2.imencode('.jpg', frame)

            input_frame = gabriel_pb2.InputFrame()
            input_frame.payload_type = gabriel_pb2.PayloadType.IMAGE
            input_frame.payloads.append(jpeg_frame.tobytes())

            extras = self.produce_extras()
            if extras is not None:
                input_frame.extras.Pack(extras)

            logger.debug(f"Sending frame {self.frames_processed}...")
            return input_frame

        return [
            ProducerWrapper(producer=producer, source_name=self._source_name)
        ]

    def consumer(self, result_wrapper):
        self.frames_processed += 1
        logger.debug(f"Received results for frame {self.frames_processed}.")
        if len(result_wrapper.results) != 1:
            logger.error('Got %d results from server',
                            len(result_wrapper.results))
            return

        result = result_wrapper.results[0]
        if result.payload_type != gabriel_pb2.PayloadType.TEXT:
            type_name = gabriel_pb2.PayloadType.Name(result.payload_type)
            logger.error('Got result of type %s', type_name)
            return
        logger.info(result.payload.decode('utf-8'))