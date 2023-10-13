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
