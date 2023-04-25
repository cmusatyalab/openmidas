import time
import os
import cv2
import numpy as np
import logging
from gabriel_server import cognitive_engine
from gabriel_protocol import gabriel_pb2
from .protocol import openmidas_pb2
from PIL import Image, ImageDraw
import torch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MiDaSEngine(cognitive_engine.Engine):
    ENGINE_NAME = "midas"

    def __init__(self, args):
        self.store_detections = args.store
        self.model = args.model
        self.valid_models = ['DPT_BEiT_L_512',
        'DPT_BEiT_L_384',
        'DPT_BEiT_384',
        'DPT_SwinV2_L_384',
        'DPT_SwinV2_B_384',
        'DPT_SwinV2_T_256',
        'DPT_Swin_L_384',
        'DPT_Next_ViT_L_384',
        'DPT_LeViT_224',
        'DPT_Large',
        'DPT_Hybrid',
        'MiDaS',
        'MiDaS_small']
        #timing vars
        self.count = 0
        self.lasttime = time.time()
        self.lastcount = 0
        self.lastprint = self.lasttime
        self.colormap = 1
        self.load_midas(self.model)

        if self.store_detections:
            self.watermark = Image.open(os.getcwd()+"/watermark.png")
            self.storage_path = os.getcwd()+"/images/"
            try:
                os.makedirs(self.storage_path)
            except FileExistsError:
                logger.info("Images directory already exists.")
            logger.info("Storing detection images at {}".format(self.storage_path))

    def load_midas(self, model):
        if torch.cuda.is_available():
                logger.info(f"pytorch is using CUDA.")
                self.device = torch.device("cuda") 
        else:
            logger.info(f"pytorch is using CPU only.")
            self.device = torch.device("cpu")

        logger.info(f"Fetching {self.model} MiDaS model from torch hub...")
        self.detector = torch.hub.load("intel-isl/MiDaS", model)
        self.model = model

        self.detector.to(self.device)
        self.detector.eval()

        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if self.model == "MiDaS_small":
            self.transform = midas_transforms.small_transform
        elif self.model == 'DPT_SwinV2_L_384' or 'DPT_SwinV2_B_384' or 'DPT_Swin_L_384':
            self.transform = midas_transforms.swin384_transform
        elif self.model == "MiDaS":
            self.transform = midas_transforms.default_transform
        elif self.model == "DPT_SwinV2_T_256":
            self.transform = midas_transforms.swin256_transform
        elif self.model == "DPT_LeViT_224":
            self.transform = midas_transforms.levit_transform
        elif self.model == "DPT_BEiT_L_512":
            self.transform = midas_transforms.beit512_transform
        else:
            self.transform = midas_transforms.dpt_transform
        logger.info("Depth predictor initialized with the following model: {}".format(model))

    def handle(self, input_frame):
        if input_frame.payload_type == gabriel_pb2.PayloadType.TEXT:
            #if the payload is TEXT, we ignore
            status = gabriel_pb2.ResultWrapper.Status.SUCCESS
            result_wrapper = cognitive_engine.create_result_wrapper(status)
            result_wrapper.result_producer_name.value = self.ENGINE_NAME
            result = gabriel_pb2.ResultWrapper.Result()
            result.payload_type = gabriel_pb2.PayloadType.TEXT
            result.payload = f'Ignoring TEXT payload.'.encode(encoding="utf-8")
            result_wrapper.results.append(result)
            return result_wrapper

        extras = cognitive_engine.unpack_extras(openmidas_pb2.Extras, input_frame)
        self.colormap = extras.colormap

        if extras.model != '' and extras.model != self.model:
            if extras.model < 0 or extras.model > len(self.valid_models):
                logger.error(f"Invalid MiDaS model {extras.model}.")
            else:
                self.load_midas(self.valid_models[extras.model])
        self.t0 = time.time()
        depth_img = self.process_image(input_frame.payloads[0])
        timestamp_millis = int(time.time() * 1000)
        status = gabriel_pb2.ResultWrapper.Status.SUCCESS
        result_wrapper = cognitive_engine.create_result_wrapper(status)
        result_wrapper.result_producer_name.value = self.ENGINE_NAME

        _, jpeg_img = cv2.imencode(".jpg", depth_img, [cv2.IMWRITE_JPEG_QUALITY, 67])
        result = gabriel_pb2.ResultWrapper.Result()
        result.payload_type = gabriel_pb2.PayloadType.IMAGE
        result.payload = jpeg_img.tostring()
       
        result_wrapper.results.append(result)

        if self.store_detections:
            filename = str(timestamp_millis) + ".jpg"
            depth_img = Image.fromarray(depth_img)
            draw = ImageDraw.Draw(depth_img)
            draw.bitmap((0,0), self.watermark, fill=None)
            path = self.storage_path  + filename
            depth_img.save(path, format="JPEG")
            logger.info("Stored image: {}".format(path))

        self.count += 1
        if self.t1 - self.lastprint > 5:
            logger.info("inference time {0:.1f} ms, ".format((self.t1 - self.t0) * 1000))
            logger.info("wait {0:.1f} ms, ".format((self.t0 - self.lasttime) * 1000))
            logger.info("fps {0:.2f}".format(1.0 / (self.t1 - self.lasttime)))
            logger.info(
                "avg fps: {0:.2f}".format(
                    (self.count - self.lastcount) / (self.t1 - self.lastprint)
                )
            )
            self.lastcount = self.count
            self.lastprint = self.t1

        self.lasttime = self.t1

        return result_wrapper

    def process_image(self, image):
        self.t0 = time.time()
        np_data = np.fromstring(image, dtype=np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        depth_img = self.inference(img)
        self.t1 = time.time()
        return depth_img

    def inference(self, img):
        """Allow timing engine to override this"""
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        frame_width = img.shape[1]
        frame_height = img.shape[0]

        input_batch = self.transform(img).to(self.device)

        with torch.no_grad():
            prediction = self.detector(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = prediction.cpu().numpy()

        depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
        depth_map = (depth_map*255).astype(np.uint8)
        full_depth_map = cv2.applyColorMap(depth_map , self.colormap)
 
        return full_depth_map
