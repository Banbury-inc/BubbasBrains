from flask import Flask, Response
import cv2
from waitress import serve
import threading
from ultralytics import YOLO

app = Flask(__name__)

# Initialize the YOLO model
model = YOLO('yolov8n.pt')

# Create a lock for thread synchronization
lock = threading.Lock()

# Initialize the camera_run flag
camera_run = False

def stop():
    print("Stopped")
@app.route("/stop")
def stop_response():
    return Response(stop(), mimetype='multipart/x-mixed-replace; boundary=frame')


def up():
    print("Moving forward")
@app.route("/up")
def up_response():
    return Response(up(), mimetype='multipart/x-mixed-replace; boundary=frame')

def down():
    print("Moving backward")
@app.route("/down")
def down_response():
    return Response(down(), mimetype='multipart/x-mixed-replace; boundary=frame')

def left():
    print("Moving left")
@app.route("/left")
def left_response():
    return Response(left(), mimetype='multipart/x-mixed-replace; boundary=frame')

def right():
    print("Moving right")
@app.route("/right")
def right_response():
    return Response(right(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
    serve(app, host="192.168.1.76", port=4000)  # Use the serve function to run your app

