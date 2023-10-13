from flask import Flask, Response, jsonify
import cv2
from waitress import serve
import threading
#from ultralytics import YOLO
import serial.tools.list_ports
import requests
import numpy as np
#import drivers
import time
import json
import subprocess
import signal
import os
#from flask_cors import CORS
import psutil
app = Flask(__name__ )

# Initialize the YOLO model
# model = YOLO('yolov8n.pt')

# Create a lock for thread synchronization
lock = threading.Lock()

# Initialize the camera_run flag
camera_run = False
# API call to retrieve CPU usage, GPU usage, etc.

@app.route("/")
def hello_world():
    data = {"message": "Hello, World!"}
    return jsonify(data)

@app.route("/getsysteminfo")
def info_response():
    print("Fetching Device Data")
    completed_process = subprocess.run(['hostname'], stdout=subprocess.PIPE, text=True, check=True)
    device_name = completed_process.stdout.strip()
    data = {"message": "Hello, World!",
           "device-name": device_name,  
            }
    print("Returning Data")
    return jsonify(data)

def initialize_camera():
    global video_capture
    video_capture = cv2.VideoCapture(0)
    return  video_capture

def generate_frames():
    while True:
        try:
            # Check if the camera opened successfully
            if video_capture is None or not video_capture.isOpened():
                raise Exception("Could not open camera.")

            with lock:
                # Capture frame-by-frame
                ret, frame = video_capture.read()

                if not ret:
                    break

                # Encode the frame as JPEG
                _, buffer = cv2.imencode('.jpg', frame)

                # Yield the frame as bytes
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


        except Exception as e:
            print("Error:", str(e))


@app.route("/videostream")
def video_stream():
    global camera_run
    global video_capture
    if not camera_run:
        video_capture = initialize_camera()
        camera_run = True

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def close_camera():
    #close the camera
    print("Camera closed")



def generate_frames_with_object_detection():
    print("Initiating Object Detection Live Stream")
    while True:
        try:
            # Check if the camera opened successfully
            if video_capture is None or not video_capture.isOpened():
                raise Exception("Could not open camera.")

            with lock:
                # Capture frame-by-frame
                ret, frame = video_capture.read()

                if not ret:
                    break

                model = YOLO('yolov8n.pt')  # load an official detection model
                results = model.track( source=frame,verbose=False, show=False, conf=0.85, tracker="bytetrack.yaml", save=False)
                annotated_frame = results[0].plot()

                _, buffer = cv2.imencode('.jpg', annotated_frame)

                # Yield the frame as bytes
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except Exception as e:
            print("Error:", str(e))



@app.route("/od-videostream")
def od_videostream():
    global camera_run
    global video_capture
    if not camera_run:
        video_capture = initialize_camera()
        camera_run = True
    return Response(generate_frames_with_object_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')



def test():

    while True:
        print("I am never ending!")           



@app.route("/test")
def test_response():
    return Response(test(), mimetype='multipart/x-mixed-replace; boundary=frame')

def close():

    serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
    baud_rate = 9600  # Adjust this to match your device's baud rate


    ser = serial.Serial(serial_port, baud_rate)
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed")




def forward2_left2():
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


@app.route("/forward2_left2")
def forward2_left2_response():
    return Response(forward2_left2(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward2_left1():
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




@app.route("/forward2_left1")
def forward2_left1_response():
    return Response(forward2_left1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward2_left0():
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


@app.route("/forward2_left0")
def forward2_left0_response():
    return Response(forward2_left0(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward2_right1():
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


@app.route("/forward2_right1")
def forward2_right1_response():
    return Response(forward2_right1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward2_right2():
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


@app.route("/forward2_right2")
def forward2_right2_response():
    return Response(forward2_right2(), mimetype='multipart/x-mixed-replace; boundary=frame')
#####################

def forward1_left2():
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


@app.route("/forward1_left2")
def forward1_left2_response():
    return Response(forward1_left2(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward1_left1():
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


@app.route("/forward1_left1")
def forward1_left1_response():
    return Response(forward1_left1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward1_left0():
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


@app.route("/forward1_left0")
def forward1_left0_respnse():
    return Response(forward1_left0(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward1_right1():
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


@app.route("/forward1_right1")
def forward1_right1_response():
    return Response(forward1_right1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward1_right2():
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


@app.route("/forward1_right2")
def forward1_right2_response():
    return Response(forward1_right2(), mimetype='multipart/x-mixed-replace; boundary=frame')
###########################

def forward0_left2():
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


@app.route("/forward0_left2")
def forward0_left2_response():
    return Response(forward0_left2(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward0_left1():
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


@app.route("/forward0_left1")
def forward0_left1_resposne():
    return Response(forward0_left1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward0_left0():
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

        
        
        

@app.route("/forward0_left0")
def forward0_left0_response():
    return Response(forward0_left0(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward0_right1():
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


@app.route("/forward0_right1")
def forward0_right1_response():
    return Response(forward0_right1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def forward0_right2():
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


@app.route("/forward0_right2")
def forward0_right2_response():
    return Response(forward0_right2(), mimetype='multipart/x-mixed-replace; boundary=frame')
###########################3#


def backward1_left2():
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


@app.route("/backward1_left2")
def backward1_left2_response():
    return Response(backward1_left2(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward1_left1():
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


@app.route("/backward1_left1")
def backward1_left1_respone():
    return Response(backward1_left1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward1_left0():
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


@app.route("/backward1_left0")
def backward1_left0_response():
    return Response(backward1_left0(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward1_right1():
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


@app.route("/backward1_right1")
def backward1_right1_respone():
    return Response(backward1_right1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward1_right2():
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


@app.route("/backward1_right2")
def backward1_right2_response():
    return Response(backward1_right2(), mimetype='multipart/x-mixed-replace; boundary=frame')
###########################################


def backward2_left2():
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


@app.route("/backward2_left2")
def backward2_left2_response():
    return Response(backward1_left2(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward2_left1():
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


@app.route("/backward2_left1")
def backward2_left1_response():
    return Response(backward2_left1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward2_left0():
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


@app.route("/backward2_left0")
def backward2_left0_response():
    return Response(backward2_left0(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward2_right1():
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


@app.route("/backward2_right1")
def backward2_right1_response():
    return Response(backward2_right1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def backward2_right2():
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


@app.route("/backward2_right2")
def backward2_right2_resposne():
    return Response(backward2_right2(), mimetype='multipart/x-mixed-replace; boundary=frame')
#








@app.route("/close")
def close_response():
    return Response(close(), mimetype='multipart/x-mixed-replace; boundary=frame')


def stop():
    print("Stopping to a speed of 0")
    count = 0
    while count < 1:
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
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
    print("Serial port closed")


@app.route("/stop")
def stop_response():
    return Response(stop(), mimetype='multipart/x-mixed-replace; boundary=frame')


def up():
    
    count = 0
    while count < 1:
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")
        secondcount = 0 
        while secondcount < 1000:
            user_input = "L400n"
            ser.write(user_input.encode('utf-8'))
            user_input = "R400n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
            # Read and display data coming back from Arduino (if available)
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting).decode('utf-8')
                print(f"Received: {received_data}")


        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")

@app.route("/up")
def up_response():
    return Response(up(), mimetype='multipart/x-mixed-replace; boundary=frame')

def up1():
    print("Moving forward at speed 1")
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
            user_input = "R300n"
            ser.write(user_input.encode('utf-8'))
            secondcount = secondcount + 1
        print("Timer finished, closing port")
        count = count + 1
    print("Serial port closed")


@app.route("/up1")
def up1_response():
    return Response(up1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def up2():
    print("Moving forward at speed 2")
    secondcount = 0 
    serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
    baud_rate = 9600  # Adjust this to match your device's baud rate
    ser = None  # Initialize ser outside of the try block
    ser = serial.Serial(serial_port, baud_rate)
 
    while secondcount < 100:
        user_input = "L400n"
        ser.write(user_input.encode('utf-8'))
        user_input = "R400n"
        ser.write(user_input.encode('utf-8'))
        secondcount = secondcount + 1
    print("Timer finished, closing port")


@app.route("/up2")
def up2_response():
    return Response(up2(), mimetype='multipart/x-mixed-replace; boundary=frame')


def down():
    print("Moving backward at speed 1")
    count = 0
    while count < 1:
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
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
    print("Serial port closed")


@app.route("/down")
def down_response():
    return Response(down(), mimetype='multipart/x-mixed-replace; boundary=frame')


def down1():

    print("Moving backward at speed 1")
    count = 0
    while count < 1:
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate
        ser = None  # Initialize ser outside of the try block
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
    print("Serial port closed")


@app.route("/down1")
def down1_response():
    return Response(down1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def down2():

    print("Moving forward at speed 2")
    secondcount = 0 
    serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
    baud_rate = 9600  # Adjust this to match your device's baud rate
    ser = None  # Initialize ser outside of the try block
    ser = serial.Serial(serial_port, baud_rate)
 
    while secondcount < 100:
        user_input = "L1n"
        ser.write(user_input.encode('utf-8'))
        user_input = "R1n"
        ser.write(user_input.encode('utf-8'))
        secondcount = secondcount + 1
    print("Timer finished, closing port")


@app.route("/down2")
def down2_response():
    return Response(down2(), mimetype='multipart/x-mixed-replace; boundary=frame')

def down3():
    print("Moving backward at speed 3")

def left():
    
    count = 0
    while count < 1:
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



@app.route("/left")
def left_response():
    return Response(left(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left1():
    print("Moving left with a speed of 1")
@app.route("/left1")
def left1_response():
    return Response(left1(), mimetype='multipart/x-mixed-replace; boundary=frame')


def right():
    count = 0
    while count < 1:
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


@app.route("/right")
def right_response():
    return Response(right(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right1():
    print("Moving right with a speed of 1")
@app.route("/right1")
def right1_response():
    return Response(right1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right2():
    print("Moving right with a speed of 2")
@app.route("/right2")
def right2_response():


    return Response(right2(), mimetype='multipart/x-mixed-replace; boundary=frame')

                    

if __name__ == "__main__":
    serve(app, host="localhost", port=4001)  # Use the serve function to run your app
    CORS(app)