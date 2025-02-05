from ultralytics import YOLO

model_path = "runs/detect/train/weights/best.pt"  # Replace with the actual path to your trained model
model = YOLO(model_path)
results = model.export(format="rknn")
