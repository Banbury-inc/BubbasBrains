
import cv2
import depthai as dai
from ultralytics import YOLO
import numpy as np

def create_pipeline():
    pipeline = dai.Pipeline()

    # Create and configure the color camera
    cam = pipeline.create(dai.node.ColorCamera)
    cam.setPreviewSize(640, 360)
    cam.setInterleaved(False)

    # Create XLinkOut for video stream
    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("preview")
    cam.preview.link(xout.input)

    return pipeline

def load_yolo_model():
    # Initialize and load the YOLO model
    model = YOLO('yolov8n.pt')  # Ensure the model file path is correct
    model.fuse()  # Optional: fuse the model for potentially better performance
    return model


def main():
    # Initialize the pipeline
    pipeline = dai.Pipeline()
    cam = pipeline.create(dai.node.ColorCamera)
    cam.setPreviewSize(640, 360)
    cam.setInterleaved(False)
    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("preview")
    cam.preview.link(xout.input)

    # Load the YOLO model
    model = YOLO('yolov8n.pt')  # Correct path to your model

    # Initialize the device with the pipeline
    with dai.Device() as device:
        device.startPipeline(pipeline)
        q = device.getOutputQueue(name="preview", maxSize=4, blocking=False)

        while True:
            frame = q.get()
            img = frame.getCvFrame()

            # Perform inference
            results = model(img)

            # Assuming results is a list of detections for the current approach
            for det in results:  # Iterate through each detection
                if isinstance(det, list) or isinstance(det, np.ndarray):
                    # Assuming each detection is structured as [x1, y1, x2, y2, conf, cls]
                    x1, y1, x2, y2, conf, cls = map(int, det[:6])
                    label = f'{model.names[cls]} {conf:.2f}'
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow("YOLO Detection - OAK-D Stream", img)

            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
    main()
