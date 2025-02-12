import cv2
import torch
import numpy as np
from torchvision import transforms
from ultralytics import YOLO 
from constants import *
import math


# Load the trained model
model_path = "runs/detect/train/weights/best.pt" 
model = YOLO(model_path)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    


    
    # Show the frame
    cv2.imshow("YOLO Detection", frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
