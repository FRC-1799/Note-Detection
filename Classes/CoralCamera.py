from ConstantsAndUtils.Constants import CameraConstants
import cv2
from ultralytics import YOLO 
import math
import Vector


class CoralCamera:
    def __init__(self, cameraIndex: int = 0, modelPath: str = "Models\BestModel.pt"):
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

            for result in results:
                for box in result.boxes:
                    conf = box.conf[0].item()
                    if conf > CameraConstants.confidenceTolerance:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls = int(box.cls[0].item())

                        centerOfCoral = ((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1)
                        coralPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * centerOfCoral[0]
                        coralYaw = CameraConstants.reefCameraVerticalAnglePerPixel * centerOfCoral[1]

                        centerPitch = CameraConstants.reefCameraHorizontalAnglePerPixel * (self.screenWidth / 2)
                        centerYaw = CameraConstants.reefCameraVerticalAnglePerPixel * (self.screenHeight / 2)

                        coralPitch = coralPitch - centerPitch
                        coralYaw = -(coralYaw - centerYaw)

                        vectorOfCoral = Vector.vector(CameraConstants.cameraPosition, coralPitch, coralYaw)

                        for increment in range(1, CameraConstants.vectorLengthToExtend, 1):
                            positionLocation = vectorOfCoral.getPoseAtStep(increment)
                            
                            for reefSection in reefHitboxes:
                                for hitbox in reefSection:
                                    print(positionLocation)
                                    if hitbox.colidePose3d(positionLocation):
                                        #print(len(reef), len(reefHitboxes))
                                        reef[reefHitboxes.index(reefSection)][reefSection.index(hitbox)] = True
                                        print(reef)
                                            

                        label = f"{self.model.names[cls]}: {round(math.degrees(coralPitch), 2), round(math.degrees(coralYaw), 2)}"

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('heheh', frame)
            cv2.waitKey(1)  # Ensures OpenCV window updates properly
