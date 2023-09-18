from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import psutil
import os
import platform
import json
import cv2
from ultralytics import YOLO
import threading



app = Flask(__name__)
CORS(app)

# Create a lock for thread synchronization
lock = threading.Lock()


@app.route("/")
def index():
    return "Extensions that can be used: <br> <br> /helloworld <br> /getjetsonmodel <br> /getdeviceinfo <br> /videostream"

@app.route("/helloworld")
def hello_world():
    response_data = {
        "Message": "Hello World",
        }
    return jsonify(response_data)
@app.route("/getjetsonmodel")
def get_jetson_model():
    with open('/proc/device-tree/model', 'r') as f:
        model = f.read().strip()
    response_data = {
        "Model": model,
        }
    return jsonify(response_data)
@app.route("/getdeviceinfo")
def get_total_storage():
    try:
        # Use the 'df' command to get information about disk space
        df_output = subprocess.check_output(['df', '-h']).decode('utf-8')
        # Extract the line containing the root filesystem
        root_fs_line = [line for line in df_output.split('\n') if '/' in line][0]
        # Split the line into columns and get the total storage (column 1)
        total_storage = root_fs_line.split()[1]
                
    except Exception as e:
        return "Storage information not available"
    try:
        # Get the memory usage information
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total
        used_memory = memory_info.used
        memory_usage_percentage = memory_info.percent

    except Exception as e:
        return {"error": "Memory information not available"}
    network_info = {}
    try:
        network_info["network_interfaces"] = psutil.net_if_stats()
        network_info["ip_addresses"] = psutil.net_if_addrs()
    except Exception as e:
        network_info["error"] = "Network information not available"
    disk_info = {}
    try:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.device] = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            }
    except Exception as e:
        disk_info["error"] = "Disk information not available"

    response_data = {
        "Total Storage": total_storage,
        "total_memory": total_memory,
        "used_memory": used_memory,
        "memory_usage_percentage": memory_usage_percentage,
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_model": platform.processor(),
        "cpu_usage": psutil.cpu_percent(interval=1, percpu=True),
        "network_info": network_info,
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.release(),
        "kernel_version": platform.uname().release,
        "uptime": psutil.boot_time(),
        "disk_info": disk_info,
        }
    
    return jsonify(response_data)
def generate_frames():
    try:
        # Open the default camera (usually /dev/video0)
        cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not cap.isOpened():
            raise Exception("Could not open camera.")

        while True:
            with lock:
                # Capture frame-by-frame
                ret, frame = cap.read()

                if not ret:
                    break

                # Encode the frame as JPEG
                _, buffer = cv2.imencode('.jpg', frame)

                # Yield the frame as bytes
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    except Exception as e:
        print("Error:", str(e))
    finally:
        # Release the camera when the generator is closed

        cap.release()
@app.route("/videostream")
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Initialize the YOLO model
model = YOLO('yolov8n.pt')
def generate_frames_with_object_detection():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Open the video file
    
    cap = cv2.VideoCapture(0)

    # Loop through the video frames
    while cap.isOpened():
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

        
@app.route("/od-videostream")
def video_stream_with_object_detection():
    return Response(generate_frames_with_object_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')
#-------------------------------------------------------------


current_video_source = "http://127.0.0.1:5000/videostream-update"  # Initial video source

# ... (Your existing route functions)

@app.route("/videostream-update")
def video_stream():
    global current_video_source  # Use the global variable for video source

    def generate_frames():
        try:
            cap = cv2.VideoCapture(current_video_source)  # Use the current video source

            if not cap.isOpened():
                raise Exception("Could not open camera.")

            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except Exception as e:
            print("Error:", str(e))
        finally:
            cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Update the video source and restart the stream for object detection
@app.route("/od-videostream-update")
def video_stream_with_object_detection():
    global current_video_source  # Use the global variable for video source

    def generate_frames_with_object_detection():
        try:
            cap = cv2.VideoCapture(current_video_source)  # Use the current video source

            if not cap.isOpened():
                raise Exception("Could not open camera.")

            while True:
                success, frame = cap.read()

                if success:
                    results = model(frame)
                    annotated_frame = results[0].plot()
                    _, buffer = cv2.imencode('.jpg', annotated_frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except Exception as e:
            print("Error:", str(e))
        finally:
            cap.release()

    return Response(generate_frames_with_object_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Update the current video source when requested
@app.route("/update-video-source", methods=["POST"])
def update_video_source():
    global current_video_source
    data = request.get_json()
    new_source = data.get("source")
    current_video_source = new_source
    return jsonify({"message": "Video source updated successfully"})

if __name__ == "__main__":
    app.run(debug=True)