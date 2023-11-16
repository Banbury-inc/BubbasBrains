

import sys
import argparse
import time
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log
from adafruit_servokit import ServoKit
import serial.tools.list_ports
from communication_agent.communication_agent import CommunicationAgent 

class VisionAgent:
    def __init__(self):
#        self.input = videoSource("/dev/video2")
#        self.output = videoOutput("webrtc://@:8554/output")
#        self.net = detectNet("ssd-mobilenet-v2", sys.argv, 0.5)
        pass

    def log_message():
        role = "Task Management Agent"
        message = "Task Management Agent Initialized"
        CommunicationAgent.log_message(role, message)
 
    def run(self):
        role = "Vision Agent"
        message = "Vision Agent Initialized"
        CommunicationAgent.log_message(role, message)
        print("Vision Agent initialized")
#        try:
#            Camera.run(self) 
#        except:
#            print("camera not working")
    def objectDetection():
        # create video sources and outputs
        input = videoSource("/dev/video2")
        output = videoOutput("webrtc://@:8554/output")
        net = detectNet("ssd-mobilenet-v2", sys.argv, 0.5)

        while True:
            img = input.Capture()
            if img is None: # timeout
                continue  
            detections = net.Detect(img)
            detectedperson = False
            for detection in detections:
                object = Object.info(net, detection)

#            CommunicationAgent.videoStream(img)
            # render the image
            output.Render(img)
            # print out performance info
#            net.PrintProfilerTimes()
            # exit on input/output EOS
            if not input.IsStreaming() or not output.IsStreaming():
                break
class Object:
    def info(net, detection):
        CLassID = detection.ClassID
        ClassName = net.GetClassDesc(detection.ClassID)
        Confidence = detection.Confidence
        Left = detection.Left
        Right = detection.Right
        Width = detection.Width
        Height = detection.Height
        Bottom = detection.Bottom
        Area = detection.Area
        Center = detection.Center
        framecenterX = 640
        ramecenterY = 360 
        centerX = 0
        centerY = 0
        centerX, centerY = Center
        return CLassID, ClassName, Confidence, Left, Right, Width, Height, Bottom, Area, Center, framecenterX, ramecenterY, centerX, centerY

