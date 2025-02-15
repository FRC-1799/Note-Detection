from ConstantsAndUtils.Constants import CameraConstants
import cv2
from ultralytics import YOLO
import math
from Classes import Vector


class CoralCamera:
    """
    Detects coral and makes a ray to said coral to see which level it is on. This data gets published to NetworkTables
    """

    def __init__(self, cameraIndex: int = 0, modelPath: str = "Models/runs/detect/train/weights/BestModel.pt"):
        self.self = self
        self.cameraIndex = cameraIndex
        
        self.model = YOLO(modelPath)
        self.screenWidth = CameraConstants.horizontalPixels
        self.screenHeight = CameraConstants.verticalPixels
        self.camera = cv2.VideoCapture(cameraIndex)

    def camera_loop(self, reef: list[list[bool]], reefHitboxes: list):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.resize(frame, (self.screenWidth, self.screenHeight)) 
            results = self.model(frame)
            vectorAlreadyCollided = False

            for result in results:
                for box in result.boxes:
                    conf = box.conf[0].item()
                    if conf > CameraConstants.confidenceTolerance:
                        # Top left X, top left Y, bottom right X, bottom right Y
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls = int(box.cls[0].item())

                        centerOfCoral = ((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1) 
                        coralPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * centerOfCoral[0]
                        coralYaw = CameraConstants.reefCameraVerticalAnglePerPixel * centerOfCoral[1]

                        centerPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * (self.screenWidth / 2)
                        centerYaw = CameraConstants.reefCameraVerticalAnglePerPixel * (self.screenHeight / 2)

                        # Adjusts the pitch and yaw so that its center (0, 0) is in the middle of the camera lens
                        coralPitch = coralPitch - centerPitch
                        coralYaw = -(coralYaw - centerYaw)

                        vectorOfCoral = Vector.vector(CameraConstants.cameraPosition, coralPitch, coralYaw)

                        # Loops again for a certain increment across the line, and the increment acts as the x value for the equation
                        for increment in range(1, CameraConstants.vectorLengthToExtend):
                            positionLocation = vectorOfCoral.getPoseAtStep(increment)
                            if vectorAlreadyCollided:
                                break
                            
                            for hitboxSection in reefHitboxes:
                                for hitbox in hitboxSection:

                                    # If the Pose3d is colliding with the hitbox, we know which level it is on, so we set that level to true
                                    if hitbox.colidePose3d(positionLocation):
                                        reef[reefHitboxes.index(hitboxSection)][hitboxSection.index(hitbox)] = True
                                        vectorAlreadyCollided = True
                                        break
                                if vectorAlreadyCollided:
                                    break
                                            

                        # Labeling of the detections
                        label = f"{self.model.names[cls]}: {round(math.degrees(coralPitch), 2), round(math.degrees(coralYaw), 2)}"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('heheh', frame)
            cv2.waitKey(1)  # Ensures OpenCV window updates properly
