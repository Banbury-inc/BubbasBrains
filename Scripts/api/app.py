from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import threading
from ultralytics import YOLO
from waitress import serve  # Import Waitress

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the YOLO model
model = YOLO('yolov8n.pt')

# Create a lock for thread synchronization
lock = threading.Lock()

# Initialize the camera_run flag
camera_run = False

def generate_frames():
    global camera_run  # Use the global camera_run variable
    cap = cv2.VideoCapture(0)

    while camera_run:
        try:
            # Check if the camera opened successfully
            if not cap.isOpened():
                raise Exception("Could not open camera.")

            while camera_run:
                with lock:
                    # Capture frame-by-frame
                    ret, frame = cap.read()

                    if not ret:
                        cap.release()
                        break

                    # Encode the frame as JPEG
                    _, buffer = cv2.imencode('.jpg', frame)

                    # Yield the frame as bytes
                    yield buffer.tobytes()

        except Exception as e:
            print("Error:", str(e))

@app.route("/")
def index():
    return("Hello World")
@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("response", {"data": "Connected"})

@socketio.on("start_stream")
def start_stream():
    global camera_run  # Use the global camera_run variable
    camera_run = True
    print("Starting camera stream")
    emit("response", {"data": "Camera stream started"})

@socketio.on("stop_stream")
def stop_stream():
    global camera_run  # Use the global camera_run variable
    camera_run = False
    print("Stopping camera stream")
    emit("response", {"data": "Camera stream stopped"})

@socketio.on("disconnect")
def handle_disconnect():
    global camera_run  # Use the global camera_run variable
    camera_run = False
    print("Client disconnected")

if __name__ == "__main__":
    # Use Waitress to serve the app
    serve(app, host="localhost", port=5000)
