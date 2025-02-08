import cv2
import torch
import numpy as np
from torchvision import transforms
from ultralytics import YOLO 
from constants import *
import math
from pyrr import ray, aabb

# Define a ray (origin, direction)
ray_origin = [0, 0, 0]
ray_direction = [1, 1, 1]

# Define an AABB (min corner, max corner)
box_min = [-1, -1, -1]
box_max = [2, 2, 2]

intersects = aabb.ray_intersect_aabb(ray_origin, ray_direction, box_min, box_max)
print("Intersects:", intersects)  # True or False


# Load the trained model
model_path = "runs/detect/train/weights/best.pt" 
model = YOLO(model_path)

cap = cv2.VideoCapture(0)
screenWidth = 640
screenHeight = 384
def convert_to_center_pos(x1, x2, y1, y2):
    xValueFromCenter = (x1 - (screenWidth / 2), x2 - (screenWidth / 2))
    yValueFromCenter= (y1 - (screenHeight / 2), y2 - (screenHeight / 2))
    return xValueFromCenter, yValueFromCenter

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (screenWidth, screenHeight)) 

    results = model(frame)

    for result in results:
        for box in result.boxes:
            conf = box.conf[0].item()
            if conf > 0.75:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0].item())

                centerOfCoral = ((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1)
                coralPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * centerOfCoral[0]
                coralYaw = CameraConstants.reefCameraVerticalAnglePerPixel * centerOfCoral[1]

                centerPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * (screenWidth / 2)
                centerYaw = CameraConstants.reefCameraVerticalAnglePerPixel * (screenHeight / 2)

                coralPitch = coralPitch - centerPitch
                coralYaw = -(coralYaw - centerYaw)


                label = f"{model.names[cls]}: {round(math.degrees(coralPitch), 2), round(math.degrees(coralYaw), 2)}"  
                
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
