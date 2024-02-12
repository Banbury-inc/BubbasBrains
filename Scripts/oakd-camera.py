import cv2
import depthai as dai

def create_pipeline():
    pipeline = dai.Pipeline()

    cam = pipeline.create(dai.node.ColorCamera)
    cam.setPreviewSize(640, 360)
    cam.setInterleaved(False)


    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("preview")
    cam.preview.link(xout.input)

    return pipeline

def main():
    pipeline = create_pipeline()
    with dai.Device(pipeline) as device:
        print("Starting pipeline...")
        device.startPipeline()

        q = device.getOutputQueue(name="preview", maxSize=4, blocking=False)

        while True:
            frame = q.get()
            img = frame .getCvFrame()

            cv2.imshow("Oak-D Stream", img)

            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    main()
