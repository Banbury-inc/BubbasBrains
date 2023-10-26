import sys
import time
import argparse
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log
from adafruit_servokit import ServoKit





# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)
elbowangle = 90
wristangle = 90
shoulderangle = 45


# Elbow
# 0 - 180
kit.servo[2].angle = elbowangle

# Wrist
# 0 - 180 
kit.servo[3].angle = wristangle

# Shoulder Movement
# 30 - 180 
kit.servo[4].angle = shoulderangle


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




        # If the object detected is a person
        if ClassName == "person":
            detectedperson = True
            if detectedperson == True:
                if centerY < 440:
                    print("The camera is too low")
                    if elbowangle == 179:
                         elbowangle = elbowangle
                    else:
                        elbowangle += 1
                    kit.servo[2].angle = elbowangle
                    time.sleep(0.01)
                if centerY > 440:
                    if centerY < 480:
                        print("The camera is juuuuuuuuust right")
                if centerY > 480:
                    print("The camera is too high")
                    if elbowangle == 1:
                         elbowangle = elbowangle
                    else:
                        elbowangle -= 1
                    kit.servo[2].angle = elbowangle
                    time.sleep(0.01)
                if centerY < 400:
                    print("The camera is too low for the person detected")
                if centerY > 400:
                    if centerY < 480:
                        print("The camera is juuuuuuuuust right for the person detected")
                if centerY > 480:
                    print("The camera is too high for the person detected")

            # vertical zones will be 0-426, 427-853, 854-1280
                if centerX < 800:
                    print("moving camera to the left")
                    if wristangle == 179:
                        wristangle = wristangle
                    else:
                        wristangle += 1
                    kit.servo[3].angle = wristangle
                    time.sleep(0.01)
                if centerX > 800:
                    if centerX < 853:
                        print("The camera does not need to be moved")
                if centerX >= 854:
                    print("movnig caamera to the right")
                    if wristangle == 1:
                        wristangle = wristangle
                    else:
                        wristangle -= 1
                    kit.servo[3].angle = wristangle
                    time.sleep(0.01)
#        if detectedperson == False:
#                wristangle = 90
 #               kit.servo[3].angle = wristangle
 #               time.sleep(0.01)
 

   

#######################################################

    top_left_height = 0
    top_left_width = 0
    bottom_right_height = 0
    bottom_right_width = 0 

    if len(xyxys) > 0 and xyxys[0].shape ==(1,4):
        numbers = xyxys[0][0]
        top_left_width, top_left_height, bottom_right_width, bottom_right_height = numbers

    # The array prints out top left corner, bottom right corner, 
        print("Top Left Width:", top_left_width)
        print("Top Left Height:", top_left_height)
        print("Bottom Right Width:", bottom_right_width)
        print("Bottom Right Height:", bottom_right_height)
        print("")
#        print(xyxys) 
        # The dimensions of the frame is 1280 x 720, so we need to figure out a way to write an if statement 
        # saying that if most of the frame is above or below the dead center, move the motor upwards or downwards.
        # Dead center horizontally is 360. We can take the average of the two points and it will either be 
        # above or below the horizontal average of 640. If that is the case, we can call a function to move
        # the motor.         

    horizontal_average = (bottom_right_height + top_left_height) / 2
    print("Horizontal Average", horizontal_average)


 ######################################################       

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
