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

    def camera_loop(self, reef: list[list[bool]], algae: list[list[bool]], reefHitboxes: list, algaeHitboxes: list, algaeNotSeenCounter: list, robotPosition):
        ret, frame = self.camera.read()


        if ret:
            frame = cv2.resize(frame, (self.screenWidth, self.screenHeight)) 
            results = self.model(frame)
            vectorAlreadyCollided = False

            for result in results:
                for box in result.boxes:
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    if conf > CameraConstants.confidenceTolerance:
                        if self.model.names[cls].lower() == "coral":

                            # Top left X, top left Y, bottom right X, bottom right Y
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            

                            centerOfCoral = ((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1) 
                            coralYaw = CameraConstants.reefCameraHorizontalAnglePerPixel * centerOfCoral[0]
                            coralPitch = CameraConstants.reefCameraVerticalAnglePerPixel * centerOfCoral[1]

                            centerYaw = CameraConstants.reefCameraHorizontalAnglePerPixel * (self.screenWidth / 2)
                            centerPitch = CameraConstants.reefCameraVerticalAnglePerPixel * (self.screenHeight / 2)

                            # Adjusts the pitch and yaw so that its center (0, 0) is in the middle of the camera lens
                            coralYaw = coralYaw - centerYaw
                            coralPitch = -(coralPitch - centerPitch)

                            vectorOfCoral = Vector.vector(robotPosition.transformBy(CameraConstants.ROBOT_TO_CAMERA_ROTATED_TRANSFORMATION), coralPitch, coralYaw)

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
                            
                            # When the loop is exited, reset this variable in order to be able to search again
                            vectorAlreadyCollided = False if vectorAlreadyCollided else True
                                                

                            # Labeling of the detections
                            label = f"{self.model.names[cls]}: {round(math.degrees(coralPitch), 2), round(math.degrees(coralYaw), 2)}"
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # else: # Is algae
                        #     x1, y1, x2, y2 = map(int, box.xyxy[0])
                            

                        #     centerOfAlgae = ((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1) 
                        #     algaeYaw = CameraConstants.reefCameraHorizontalAnglePerPixel * centerOfAlgae[0]
                        #     algaePitch = CameraConstants.reefCameraVerticalAnglePerPixel * centerOfAlgae[1]

                        #     centerYaw = CameraConstants.reefCameraHorizontalAnglePerPixel * (self.screenWidth / 2)
                        #     centerPitch = CameraConstants.reefCameraVerticalAnglePerPixel * (self.screenHeight / 2)

                        #     # Adjusts the pitch and yaw so that its center (0, 0) is in the middle of the camera lens
                        #     algaeYaw = algaeYaw - centerYaw
                        #     algaePitch = -(algaePitch - centerPitch)

                        #     vectorOfAlgae = Vector.vector(robotPosition.transformBy(CameraConstants.ROBOT_TO_CAMERA_ROTATED_TRANSFORMATION), algaePitch, algaeYaw)

                        #     for increment in range(1, CameraConstants.vectorLengthToExtend):
                        #         positionLocation = vectorOfAlgae.getPoseAtStep(increment)
                        #         if vectorAlreadyCollided:
                        #             break
                                
                        #         for hitboxSection in algaeHitboxes:
                        #             for hitbox in hitboxSection:

                        #                 hitboxSectionIndex = algaeHitboxes.index(hitboxSection)
                        #                 hitboxIndex = hitboxSection.index(hitbox)
                        #                 algaeSeen = hitbox.colidePose3d(positionLocation)

                        #                 # If we haven't seen the algae for more than the tolerance frames, it is not seen right now, and it is marked as true, then assume it isn't there anymore
                        #                 if algaeNotSeenCounter[hitboxSectionIndex][hitboxIndex] > CameraConstants.algaeViewedTolerance and not algaeSeen and algae[hitboxSectionIndex][hitboxIndex]:
                        #                     algae[hitboxSectionIndex][hitboxSection] = False
                                        
                        #                 # If we do see the algae and it is false, mark it as true
                        #                 if algaeSeen and not algae[hitboxSectionIndex][hitboxIndex]:
                        #                     algae[hitboxSectionIndex][hitboxIndex] = True
                        #                     vectorAlreadyCollided = True
                        #                     break

                        #                 # If we don't see the algae, but it is marked as true, increase the counter
                        #                 elif not algaeSeen and algae[hitboxSectionIndex][hitboxIndex]:
                        #                     algaeNotSeenCounter[hitboxSectionIndex][hitboxIndex] += 1
                        #             if vectorAlreadyCollided:
                        #                 break
                            
                        #     # When the loop is exited, reset this variable in order to be able to search again
                        #     vectorAlreadyCollided = False if vectorAlreadyCollided else True


            cv2.imshow('heheh', frame)
            cv2.waitKey(1)  # Ensures OpenCV window updates properly
