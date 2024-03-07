import sys
import time
import argparse
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log
from adafruit_servokit import ServoKit
import serial.tools.list_ports

'''
To run:

python3 followmode_wheels.py /dev/video2

or to stream to a website

python3 followmode_wheels.py /dev/video2 webrtc://@:8554/output

'''


# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)
	
# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

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
        break
