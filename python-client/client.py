#!/usr/bin/env python3

# Copyright 2021 Carnegie Mellon University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import cv2
from gabriel_client.websocket_client import WebsocketClient
from gabriel_client.opencv_adapter import OpencvAdapter
from gabriel_protocol import gabriel_pb2
import logging
from zmq_adapter import ZmqAdapter
import openscout_pb2
import uuid
import geocoder

UUID = str(uuid.uuid4())
WEBSOCKET_PORT = 9099
DEFAULT_SOURCE_NAME = 'openscout'

logger = logging.getLogger(__name__)
logging.getLogger("geocoder").setLevel(logging.WARNING)

def preprocess(frame):
    return frame

def produce_extras():
    extras = openscout_pb2.Extras()
    extras.client_id = UUID
    g = geocoder.ip('me')
    extras.location.latitude = g.latlng[0]
    extras.location.longitude = g.latlng[1]
    extras.model = 'coco'
    return extras

def local_consumer(result_wrapper):
    if len(result_wrapper.results) != 1:
        logger.debug('Got %d results from server',
                        len(result_wrapper.results))
        return

    result = result_wrapper.results[0]
    if result.payload_type != gabriel_pb2.PayloadType.TEXT:
        type_name = gabriel_pb2.PayloadType.Name(result.payload_type)
        logger.error('Got result of type %s', type_name)
        return
    logger.info(result.payload.decode('utf-8'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', default='openscout-demo.cmusatyalab.org',
        help='Specify address of OpenScout server [default: openscout-demo.cmusatyalab.org')
    parser.add_argument('-p', '--port', default='9099', help='Specify websocket port [default: 9099]')
    parser.add_argument('-c', '--camera', action='store_true', help='Use cv2.VideoCapture(0) adapter instead of ZmqAdapter')
    parser.add_argument('-d', '--display', action='store_true', help='Optionally display the frames received by the ZmqAdapter using cv2.imshow')
    parser.add_argument('-l', '--loglevel', default='INFO', help='Set the log level')
    
    args = parser.parse_args()
    logging.basicConfig(format="%(levelname)s: %(message)s", level=args.loglevel)
    if args.camera:
        capture = cv2.VideoCapture(0)
        adapter = OpencvAdapter(
            preprocess, produce_extras, None, capture, DEFAULT_SOURCE_NAME)
    else:
        adapter = ZmqAdapter(preprocess, DEFAULT_SOURCE_NAME, args.display)

    client = WebsocketClient(
        args.server, args.port,
        adapter.get_producer_wrappers(), local_consumer if args.camera else adapter.consumer
    )
    client.launch()


if __name__ == '__main__':
    main()