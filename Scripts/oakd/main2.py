#!/usr/bin/env python3
import blobconverter
import cv2
import depthai as dai
import numpy as np
import math


nnBlobPath = blobconverter.from_zoo(name='mobilenet-ssd', shaves=4)

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
spatialDetectionNetwork = pipeline.create(dai.node.MobileNetSpatialDetectionNetwork)
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)
spatialLocationCalculator = pipeline.create(dai.node.SpatialLocationCalculator)

xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutNN = pipeline.create(dai.node.XLinkOut)
xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutSpatialData = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
xoutNN.setStreamName("detections")
xoutDepth.setStreamName("depth")
xoutSpatialData.setStreamName("spatialData")

# Properties
camRgb.setPreviewSize(300, 300)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
stereo.setLeftRightCheck(True)
stereo.setSubpixel(True)

# Spatial detection network model settings
spatialDetectionNetwork.setBlobPath(nnBlobPath)
spatialDetectionNetwork.setConfidenceThreshold(0.5)
spatialDetectionNetwork.input.setBlocking(False)
spatialDetectionNetwork.setBoundingBoxScaleFactor(0.5)
spatialDetectionNetwork.setDepthLowerThreshold(100)
spatialDetectionNetwork.setDepthUpperThreshold(5000)

# Linking
monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

camRgb.preview.link(spatialDetectionNetwork.input)
spatialDetectionNetwork.passthrough.link(xoutRgb.input)
spatialDetectionNetwork.out.link(xoutNN.input)

stereo.depth.link(spatialDetectionNetwork.inputDepth)
stereo.depth.link(xoutDepth.input)
stereo.depth.link(spatialLocationCalculator.inputDepth)

# Configure the spatialLocationCalculator
config = dai.SpatialLocationCalculatorConfig()

for i in range(10):
    cfg = dai.SpatialLocationCalculatorConfigData()
    cfg.depthThresholds.lowerThreshold = 200
    cfg.depthThresholds.upperThreshold = 10000
    # Define a grid of ROIs across the depth map
    cfg.roi = dai.Rect(dai.Point2f(0.1 * i, 0.4), dai.Point2f(0.1 * (i + 1), 0.6))
    spatialLocationCalculator.initialConfig.addROI(cfg)
    config.addROI(cfg)

#spatialLocationCalculator.initialConfig

spatialLocationCalculator.out.link(xoutSpatialData.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    previewQueue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    detectionNNQueue = device.getOutputQueue(name="detections", maxSize=4, blocking=False)
    depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
    spatialDataQueue = device.getOutputQueue(name="spatialData", maxSize=4, blocking=False)
    color = (0,200,40)
    fontType = cv2.FONT_HERSHEY_TRIPLEX
    while True:
        inPreview = previewQueue.get()
        inDet = detectionNNQueue.get()
        inDepth = depthQueue.get()
        inSpatialData = spatialDataQueue.get()

        frame = inPreview.getCvFrame()
        depthFrame = inDepth.getFrame()  # depthFrame values are in millimeters

        depthFrameColor = cv2.normalize(depthFrame, None, 0, 255, cv2.NORM_MINMAX)
        depthFrameColor = np.ascontiguousarray(depthFrameColor, dtype=np.uint8)
        depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)

        # Draw ROI grid
        spatialData = inSpatialData.getSpatialLocations()
        for data in spatialData:
            roi = data.config.roi
            roi = roi.denormalize(depthFrameColor.shape[1], depthFrameColor.shape[0])

            xmin = int(roi.topLeft().x)
            ymin = int(roi.topLeft().y)
            xmax = int(roi.bottomRight().x)
            ymax = int(roi.bottomRight().y)

            coords = data.spatialCoordinates
            distance = math.sqrt(coords.x ** 2 + coords.y ** 2 + coords.z ** 2)

            

            topLeft = roi.topLeft()
            bottomRight = roi.bottomRight()
            cv2.rectangle(depthFrameColor, (int(topLeft.x), int(topLeft.y)), (int(bottomRight.x), int(bottomRight.y)), (255, 0, 0), 2)
            cv2.putText(depthFrameColor, "{:.1f}m".format(distance/1000), (xmin + 10, ymin + 20), fontType, 0.6, color)

        desired_size = (1024, 576)
        frame_resized = cv2.resize(frame , desired_size)
        depthFrameColor_resized = cv2.resize(depthFrameColor, desired_size)
        combined_image = np.vstack((frame_resized, depthFrameColor_resized))


        #cv2.imshow("rgb", frame)
        #cv2.imshow("depth", depthFrameColor)
        cv2.imshow("Combined", combined_image)

        if cv2.waitKey(1) == ord('q'):
            break

