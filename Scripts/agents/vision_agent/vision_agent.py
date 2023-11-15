

import sys
import argparse
from communication_agent.communication_agent import CommunicationAgent
from vision_agent.camera import Camera
import time
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log
from adafruit_servokit import ServoKit
import serial.tools.list_ports






class VisionAgent:
    def __init__(self):
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
        try:
            Camera.run(self) 
        except:
            print("camera not working")






'''
To run:

python3 followmode_wheels.py /dev/video2

or to stream to a website

python3 followmode_wheels.py /dev/video2 webrtc://@:8554/output

'''

# create video sources and outputs
input = videoSource("/dev/video2")
output = videoOutput("webrtc://@:8554/output")
	
# load the object detection network
net = detectNet("ssd-mobilenet-v2", sys.argv, 0.5)
# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

# process frames until EOS or the user exits
serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
baud_rate = 115200  # Adjust this to match your device's baud rate
ser = serial.Serial(serial_port, baud_rate)
print(f"Connected to {serial_port} at {baud_rate} baud")



while True:
    # capture the next image
  #  img = input.Capture()
    img = input.Capture()

    if img is None: # timeout
        continue  
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))
    xyxys = []


    detectedperson = False
    for detection in detections:
        # the options that we have to extract from detections are
        # ClassID, Confidence, Left, Right, Width, Height, Bottom, Area and Center.
        print(detection.ClassID)
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
        print(ClassName) 
        print(detection)
        framecenterX = 640
        ramecenterY = 360 
        centerX = 0
        centerY = 0
        centerX, centerY = Center
        print(centerX)
        print(centerY)
        print(Area)




        # If the object detected is a person
        if ClassName == "person":
            detectedperson = True
            if detectedperson == True:
            # vertical zones will be 0-426, 427-853, 854-1280
            # vertical zones will be 0-426, 533-746, 854-1280

                        if Area < 50000:
                            print("Bubbabot needs to move closer") 
                            if centerX < 533:
                                print("moving to the left")
                                user_input = "L6"
                                ser.write(user_input.encode('utf-8'))
                                user_input = "R7"
                                ser.write(user_input.encode('utf-8'))
                            if centerX >= 533:
                                if centerX < 746:
                                    print("Bubbabot does not need to rotate")
                                    user_input = "L7"
                                    ser.write(user_input.encode('utf-8'))
                                    user_input = "R7"
                                    ser.write(user_input.encode('utf-8'))
                                if centerX >= 746:
                                            print("moving to the right")
                                            user_input = "L7"
                                            ser.write(user_input.encode('utf-8'))
                                            user_input = "R6"
                                            ser.write(user_input.encode('utf-8'))
                        if Area > 50000:
                            if Area < 80000:
                                print("Bubbabot is a good distance")
                                if centerX < 533:
                                            print("moving to the left")
                                            user_input = "L2"
                                            ser.write(user_input.encode('utf-8'))
                                            user_input = "R6"
                                            ser.write(user_input.encode('utf-8'))
                                if centerX >= 533:
                                    if centerX < 746:
                                        print("Bubbabot does not need to rotate")
                                        user_input = "L5"
                                        ser.write(user_input.encode('utf-8'))
                                        user_input = "R5"
                                        ser.write(user_input.encode('utf-8'))
                                    if centerX >= 746:
                                        print("moving to the right")
                                        user_input = "L6"
                                        ser.write(user_input.encode('utf-8'))
                                        user_input = "R2"
                                        ser.write(user_input.encode('utf-8'))
                            if Area > 80000:
                                print("Bubbabot is too close")
                                if centerX < 533:
                                    print("moving to the left")
                                    user_input = "L1"
                                    ser.write(user_input.encode('utf-8'))
                                    user_input = "R3"
                                    ser.write(user_input.encode('utf-8'))
                                if centerX >= 533:
                                    if centerX < 746:
                                        print("Bubbabot does not need to rotate")
                                        user_input = "L1"
                                        ser.write(user_input.encode('utf-8'))
                                        user_input = "R1"
                                        ser.write(user_input.encode('utf-8'))
                                    if centerX >= 746:
                                        print("moving to the right")
                                        user_input = "L3"
                                        ser.write(user_input.encode('utf-8'))
                                        user_input = "R1"
                                        ser.write(user_input.encode('utf-8'))




    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        b