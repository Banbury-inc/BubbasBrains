from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov8n.pt')
model.fuse()

results = model.track(source=0, show=True, conf=0.8, save=False, persist=True, tracker="bytetrack.yaml")