from depthai_sdk import OakCamera
from depthai_sdk.visualize.configs import BboxStyle, TextPosition
from depthai_sdk.classes import DetectionPacket
from depthai_sdk.visualize.visualizer_helper import FramePosition, VisualizerHelper
import cv2

def print_num_objects(packet):
    print(f'Number of objects detected: {len(packet.detections)}')
    packet.decode()


with OakCamera() as oak:
    color = oak.create_camera('color', resolution='1080p')
    # List of models that are supported out-of-the-box by the SDK:
    # https://docs.luxonis.com/projects/sdk/en/latest/features/ai_models/#sdk-supported-models
    yolo = oak.create_nn('yolov6n_coco_640x640', input=color)
    oak.callback(yolo, callback=print_num_objects)
    visualizer = oak.visualize(yolo)
    oak.start(blocking=True)


