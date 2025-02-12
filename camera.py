from constants import CameraConstants
import cv2
from ultralytics import YOLO 
from vector import vector


class CoralCamera:
    def __init__(self, cameraIndex: int = 0, modelPath: str = "runs/detect/train/weights/best.pt"):
        self.self = self
        self.cameraIndex = cameraIndex
        
        self.model = YOLO(modelPath)
        self.screenWidth = CameraConstants.horizontalPixels 
        self.screenHeight = CameraConstants.verticalPixels
        self.camera = cv2.VideoCapture(cameraIndex)

    def camera_loop(self, reef: list, reefHitboxes: list):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.resize(frame, (self.screenWidth, self.screenHeight)) 

            results = self.model(frame)

            for result in results:
                for box in result.boxes:
                    conf = box.conf[0].item()
                    if conf > CameraConstants.confidenceTolerance:
                        # Coral's top left x, top right y, bottom right x, and bottom right y position
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls = int(box.cls[0].item())

                        centerOfCoral = ((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1)
                        coralPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * centerOfCoral[0]
                        coralYaw = CameraConstants.reefCameraVerticalAnglePerPixel * centerOfCoral[1]

                        centerPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * (self.screenWidth / 2)
                        centerYaw = CameraConstants.reefCameraVerticalAnglePerPixel * (self.screenHeight / 2)

                        # Adjusted so that (0, 0) is the middle of the screen, instead of it being the top left corner
                        coralPitch = coralPitch - centerPitch
                        coralYaw = -(coralYaw - centerYaw)

                        vector = vector(CameraConstants.cameraPosition, coralPitch, coralYaw) # draws the vector

                        
                        for increment in range(1, CameraConstants.vectorLengthToExtend, 1): # increase by the lenght by an increment
                            positionLocation = vector.getPoseAtStep(increment)
                            for reefSection in reefHitboxes:
                                for hitbox in reefSection:
                                    if hitbox.colidePose3d(positionLocation): # check if the point is inside of the reef's hitbox
                                        reef[reefHitboxes.index(reefSection)][reefSection.index(hitbox)] = True
                                    
                        label = f"{self.model.names[cls]}: {round(self.math.degrees(coralPitch), 2), round(self.math.degrees(coralYaw), 2)}"  
                        
                        # Draw rectangle and label
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)