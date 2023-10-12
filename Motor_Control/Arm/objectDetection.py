import cv2
import numpy as np
from adafruit_servokit import ServoKit

# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)

# Load the YOLO model
net = cv2.dnn.readNet("yolov8n.pt")  # Replace with your YOLO model and configuration files
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Open a video capture source (0 for the default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Detect objects using YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Process YOLO output to get detected objects
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Keep only 'person' detections
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(class_ids[i])
            confidence = confidences[i]
            if label == '0':  # '0' corresponds to 'person' class in YOLO
                # Calculate the position of the detected person and adjust servo angles
                calculated_pan_angle = (x + w / 2) * 180 / width
                calculated_tilt_angle = (y + h / 2) * 180 / height
                kit.servo[2].angle = calculated_pan_angle
                kit.servo[3].angle = calculated_tilt_angle

    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
