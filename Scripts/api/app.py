from flask import Flask, Response
import cv2
from waitress import serve
import threading
# from ultralytics import YOLO
import serial.tools.list_ports
#import drivers
import time


app = Flask(__name__ )

# Initialize the YOLO model
# model = YOLO('yolov8n.pt')

# Create a lock for thread synchronization
lock = threading.Lock()

# Initialize the camera_run flag
camera_run = False

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
        while secondcount < 100:
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

def left2():
    print("Moving left with a speed of 2")
@app.route("/left2")
def left2_response():
    return Response(left1(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left3():
    print("Moving left with a speed of 3")
@app.route("/left3")
def left3_response():
    return Response(left3(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left4():
    print("Moving left with a speed of 4")
@app.route("/left4")
def left4_response():
    return Response(left4(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left5():
    print("Moving left with a speed of 5")
@app.route("/left5")
def left5_response():
    return Response(left5(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left6():
    print("Moving left with a speed of 6")
@app.route("/left6")
def left6_response():
    return Response(left6(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left7():
    print("Moving left with a speed of 7")
@app.route("/left7")
def left7_response():
    return Response(left7(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left8():
    print("Moving left with a speed of 8")
@app.route("/left8")
def left8_response():
    return Response(left8(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left9():
    print("Moving left with a speed of 9")
@app.route("/left9")
def left9_response():
    return Response(left9(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left10():
    print("Moving left with a speed of 10")
@app.route("/left10")
def left10_response():
    return Response(left10(), mimetype='multipart/x-mixed-replace; boundary=frame')


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

def right3():
    print("Moving right with a speed of 3")
@app.route("/right3")
def right3_response():
    return Response(right3(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right4():
    print("Moving right with a speed of 4")
@app.route("/right4")
def right4_response():
    return Response(right4(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right5():
    print("Moving right with a speed of 5")
@app.route("/right5")
def right5_response():
    return Response(right5(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right6():
    print("Moving right with a speed of 6")
@app.route("/right6")
def right6_response():
    return Response(right6(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right7():
    print("Moving right with a speed of 7")
@app.route("/right7")
def right7_response():
    return Response(right7(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right8():
    print("Moving right with a speed of 8")
@app.route("/right8")
def right8_response():
    return Response(right8(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right9():
    print("Moving right with a speed of 9")
@app.route("/right9")
def right9_response():
    return Response(right9(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right10():
    print("Moving right with a speed of 10")
@app.route("/right10")
def right10_response():
    return Response(right10(), mimetype='multipart/x-mixed-replace; boundary=frame')

def initialize_camera():
    global video_capture
    video_capture = cv2.VideoCapture(0)

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
    if not camera_run:
        initialize_camera()
        camera_run = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames_with_object_detection():
    global camera_run  # Use the global camera_run variable
    while camera_run:
        # Load the YOLOv8 model
        # Open the video file
        # Close the current stream (if it's open)
        try:
            # Open the default camera (usually /dev/video0)
            cap = cv2.VideoCapture(0)

            # Check if the camera opened successfully
            if not cap.isOpened():
                raise Exception("Could not open camera.")

            # Loop through the video frames
            while camera_run:
                # Read a frame from the video
                success, frame = cap.read()

                if success:
                    with lock:
                        # Run YOLOv8 inference on the frame
                        results = model(frame)

                        # Visualize the results on the frame
                        annotated_frame = results[0].plot()

                        # Encode the frame as JPEG
                        _, buffer = cv2.imencode('.jpg', annotated_frame)

                        # Yield the frame as bytes
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            print("Error:", str(e))

@app.route("/od-videostream")
def od_videostream():
    global camera_run  # Use the global camera_run variable
    camera_run = True
    return Response(generate_frames_with_object_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ... (Your existing routes and code)

                    

if __name__ == "__main__":
    serve(app, host="192.168.1.51", port=4001)  # Use the serve function to run your app

