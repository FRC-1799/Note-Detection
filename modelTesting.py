import cv2
import torch
import numpy as np
from torchvision import transforms
from ultralytics import YOLO  # Ensure you have ultralytics installed (pip install ultralytics)

# Load the trained model
model_path = "runs/detect/train/weights/best.pt"  # Replace with the actual path to your trained model
model = YOLO(model_path)  # Load YOLOv8 model (Ultralytics)

# Open video file
video_path = "testvid.mp4"  # Replace with the actual path to your video file
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Run the model on the frame
    results = model(frame)
    
    # Draw bounding boxes
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0].item()  # Confidence score
            cls = int(box.cls[0].item())  # Class index
            label = f"{model.names[cls]}: {conf:.2f}"  # Get class name and confidence
            
            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Show the frame
    cv2.imshow("YOLO Detection", frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
