from ultralytics import YOLO

# Load a pre-trained YOLOv8 model (if training from scratch)
model = YOLO("yolov8n.pt")  # Use yolov8s.pt for a larger model

# Train the model using your dataset
model.train(data="C:/Users/brenn/Downloads/ReefModel/data.yaml", epochs=5, imgsz=640)