

from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official detection model
# model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
#model = YOLO('path/to/best.pt')  # load a custom model

# Track with the model
# results = model(source="https://youtu.be/Zgi9g1ksQHc", show=True, conf=0.4, save=True)


results = model(source=0, show=True, conf=0.8, save=True)