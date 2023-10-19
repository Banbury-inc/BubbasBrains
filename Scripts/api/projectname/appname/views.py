from rest_framework import generics
from .models import Item
import serial.tools.list_ports
from .serializers import ItemSerializer
from django.http import JsonResponse
from django.http import HttpResponse
import sys
import os
from django.shortcuts import render
import get_system_info
import cv2
from adafruit_servokit import ServoKit
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
def index(request):
    return render(request, 'Manual_Control_dev.html')
def test(request):
    response = "Hello World"
    return JsonResponse({'result' : response})
def getSystemInfo(request):
    response = get_system_info.get_device_name()
    return JsonResponse({'result' : response})
def followMode(request):
    response = followMode()
    return JsonResponse({'result' : response})
def initialize(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    elbowangle = 0
    wristangle = 0
    shoulderangle = 50
    kit.servo[4].angle = shoulderangle
    kit.servo[2].angle = elbowangle
    kit.servo[3].angle = wristangle
def moveShoulderUp(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    shoulderangle = 0
    kit.servo[4].angle = shoulderangle
def moveShoulderDown(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    shoulderangle = 180
    kit.servo[4].angle = shoulderangle
def moveElbowUp(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    elbowangle = 0
    kit.servo[2].angle = elbowangle
def moveElbowDown(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    elbowangle = 180 
    kit.servo[2].angle = elbowangle
def moveWristUp(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    wristangle = 0
    kit.servo[3].angle = wristangle
def moveWristDown(request):
    print("Initializing Arm")
    kit = ServoKit(channels=16)
    wristangle = 180
    kit.servo[3].angle = wristangle
from django.http import StreamingHttpResponse
import cv2

# A generator function that yields video frames
def generate_video_frames():
    video_capture = cv2.VideoCapture(0)
    while True:
        try:
            if video_capture is None or not video_capture.isOpened():
                raise Exception("Could not open camera.")

            ret, frame = video_capture.read()

            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)

            # Yield the frame as bytes with the appropriate MIME headers
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            print("Error:", str(e))

# A Django view that returns the video stream
def videostream(request):
    # Set the content type to multipart/x-mixed-replace
    response = StreamingHttpResponse(generate_video_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
    
    return response

def forward2_left2(request):
    print("2,-2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L300n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R400n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward2_left1(request):
    print("2,-1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L350n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R400n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward2_left0(request):
    print("2,0")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L400n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R400n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    ser.close()
    print("Serial port closed")
def forward2_right1(request):
    print("2,1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L400n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R350n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward2_right2(request):
    print("2,2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L400n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R300n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward1_left2(request):
    print("1,-2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L200n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R300n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward1_left1(request):
    print("1,-1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L240n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R300n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward1_left0(request):
    print("1,0")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L300n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R300n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    ser.close()
    print("Serial port closed")
def forward1_right1(request):
    print("1,1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L300n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R240n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward1_right2(request):
    print("1,2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L300n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R200n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward0_left2(request):
    print("0,-2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L1n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R400n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward0_left1(request):
    print("0,-1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L100n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R300"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward0_left0(request):
    print("0,0")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L200n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R200n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    ser.close()
    print("Serial port closed")
def forward0_right1(request):
    print("0,1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L300n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R100n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def forward0_right2(request):
    print("0,2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L400n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R1n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward1_left2(request):
    print("-1 ,-2") 
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L200n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R100n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward1_left1(request):
    print("-1,-1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L150n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R100n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward1_left0(request):
    print("-1,0")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L100n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R100n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    ser.close()
    print("Serial port closed")
def backward1_right1(request):
    print("-1,1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L100n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R150n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    ser.close()
    print("Serial port closed")
def backward1_right2(request):
    print("-1,2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L100n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R200n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward2_left2(request):
    print("-2 ,-2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L100n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R1n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward2_left1(request):
    print("-2,-1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L50n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R1n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward2_left0(request):
    print("-2,0")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L1n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R1n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    ser.close()
    print("Serial port closed")
def backward2_right1(request):
    print("-2,1")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L1n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R50n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")
def backward2_right2(request):
    print("-2,2")
    count = 0
    while count < 1:
        global ser
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 100:
            user_input = "L1n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R100n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")

















