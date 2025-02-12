import robotpy_apriltag as apriltag
import constants
import math

from typing import Optional
from photonlibpy.estimatedRobotPose import EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
from wpimath.geometry import Transform3d, Pose2d, Pose3d, Translation3d
from photonlibpy.photonTrackedTarget import TargetCorner


class AprilTagCamera:

    def __init__(self, cameraName: str):
        """
        When initialized, a PhotonCamera will be created, along with a PhotonPoseEstimator if the camera being passed is supposed to detect April Tags.

        Parameters:
        cameraName  (str): Name of a camera in String format. Used to find which camera is being used in Photon Vision.
        cameraType (str): Optional Parameter that is what the camera will be doing. If it is detecting April Tags, pass Pose in for it, and leave the parameter blank if it is detecting objects.
        """

        self.cameraName = cameraName
        self.camera = PhotonCamera(self.cameraName)
        self.estimator = PhotonPoseEstimator(
            apriltag.loadAprilTagLayoutField(apriltag.AprilTagField.k2024Crescendo),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self.camera,
            constants.CameraConstants.ROBOT_TO_CAMERA_TRANSFORMATION,
        )

        self.estimator.multiTagFallbackStrategy = PoseStrategy.LOWEST_AMBIGUITY

    def get_estimated_global_pose(self) -> Optional[EstimatedRobotPose]:
        return self.estimator.update()

    def get_estimated_global_pose_2d(self) -> Optional[Pose2d]:
        result = self.estimator.update()
        if result:
            return result.estimatedPose.toPose2d()


    def get_tags(self) -> dict[int, Transform3d]:
        """
        Gets April Tags found in the camera and returns them with their id number and estimated location.

        Returns:
        Dictionary[integer, Transform3d]: The integer is the ID for the April Tag and the Transform3d is the position of the tag
        """

        photon_result = self.camera.getLatestResult()
        resultTargets = photon_result.getTargets()
        tags = {}
        for target in resultTargets:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > 0.2:
                continue

            tags[target.fiducialId] = target.bestCameraToTarget

        return tags

    def fetch_robot_position(self):
        position = self.get_estimated_global_pose()  # Get robot position
        return position

class CoralCamera:
    def __init__(self, cameraName, team):
        self.cameraName = cameraName
        self.camera = PhotonCamera(self.cameraName)
        self.team = team

    def get_targets(self):
        """
        Gathers the targets located in the camera. In this case
        """

        photonResult = self.camera.getLatestResult()
        targets = photonResult.getTargets()
        #print(targets)

        self.targets = []
        for target in targets:
            print("jehu")
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > constants.PhotonLibConstants.POSE_AMBIGUITY_TOLERANCE:
                continue

            self.targets.append(target.bestCameraToTarget)

        return self.targets


    def coral_reef_location(self, reefFilledList, coralPositions):
        self.coralOnReefs = []
        copiedReefList = reefFilledList

        for coralPose in coralPositions:
            if not self.__coral_xy_in_reef(coralPose):
                return None
            for levelIndex, level in enumerate(self.reef):
                for reefPose in level:
                    coralInReef = True if coralPose.X() > reefPose.X() and coralPose.X() < reefPose.X() + constants.PhotonLibConstants.REEF_WIDTH and coralPose.Y() > reefPose.Y() and coralPose.Y() < reefPose.Y() + reefPose.Y() + constants.PhotonLibConstants.REEF_WIDTH and coralPose.Z() > reefPose.Z() and coralPose.Z() < reefPose.Z() + reefPose.Z() + constants.PhotonLibConstants.REEF_HEIGHT else False
                    copiedReefList[levelIndex][level.index(reefPose)] = 1 if coralInReef else 0

        return copiedReefList

    

class CoralCalculator:
    def __init__(self, team):
        self.team = team

    def reefs_with_coral(self, aprilTagIndex: int, reefs: list[TargetCorner], corals: list[TargetCorner]):
        

        # for reef in reefs:
        #     reefRect = reef.getMinAreaRectCorners()
        #     for sortedReef in sortedReefs:
        #         sortedReefRect = sortedReef.getMinAreaRectCorners()
        #         if sortedReefRect[2].y < reefRect[2].y:
        #             sortedReefs.insert(sortedReefs.index(sortedReef), reefRect)

        #     # If the lowest sorted reef is still higher than the reef, appened said reef to the end of sortedReefs
        #     if sortedReefRect[2].y > reefRect[2].y:
        #         sortedReefs.append(reef)

        coralAndReefs = []
        reefCopy = reef

        for coral in corals:
            for reef in reefs:
                # Makes a list of the corals and the reefs
                coralRect, reefRect = coral.getMinAreaRectCorners(), reef.getMinAreaRectCorners()
                coralOnReef = self.__rect_touching_another_rect(reefRect, coralRect)
                if coralOnReef:
                    if coralRect[0].y >= reefRect[0].y:
                        # Combined the coral and reefs to create a larger hitbox so even if the coral 
                        # covers the reef, the reef's position will still be recognized
                        reefAndCoralRect = [TargetCorner(coralRect[0].x, coralRect[0].y), 
                                            TargetCorner(coralRect[1].x, coralRect[1].y),
                                            TargetCorner(reefRect[2].x, reefRect[2].y),
                                            TargetCorner(reefRect[3].x, reefRect[3].y)]
                        coralAndReefs.append(reefAndCoralRect)
                    elif coralRect[0].y < reefRect[0].y:
                        reefAndCoralRect = [TargetCorner(reefRect[0].x, reefRect[0].y), 
                                            TargetCorner(reefRect[1].x, reefRect[1].y),
                                            TargetCorner(coralRect[2].x, coralRect[2].y),
                                            TargetCorner(coralRect[3].x, coralRect[3].y)]
                        coralAndReefs.append(reefAndCoralRect)
                else:
                    # Since there is no coral on the reef, we just append it to the rects
                    coralAndReefs.append(reef)


        coralPositions = []
        xpos = None # 0 is left, 1 is right
        ypos = None # level 2 is level 2

        # Takes of each of the positions of the coral and appends them to coralPositions
        for reefOrCoral in coralAndReefs:
            reefRect = reefOrCoral.getMinAreaRectCorners()
            coralAndReefs.remove(reefOrCoral) # we dont want to check this value, as reflexive property

            mostLeftValue = [
                True if reefRect[0].x - constants.PhotonLibConstants.REEF_X_TOLERANCE < xVal[0].x else False
                for xVal in coralAndReefs
            ]
            mostRightValue = [
                True if reefRect[1].x + constants.PhotonLibConstants.REEF_X_TOLERANCE > xVal[1].x else False
                for xVal in coralAndReefs
            ]
            closestToTop = [
                True if reefRect[0].y - constants.PhotonLibConstants.REEF_Y_TOLERANCE < xVal[0].y else False
                for xVal in coralAndReefs
            ]
            closestToBottom = [
                True if reefRect[2].y + constants.PhotonLibConstants.REEF_Y_TOLERANCE > xVal[2].y else False
                for xVal in coralAndReefs
            ]

            if reefOrCoral in corals:
                xpos = 0 if all(mostLeftValue) else 1 if all(mostRightValue) else None
                ypos = 4 if all(closestToTop) else 2 if all(closestToBottom) else 3

            if xpos != None and ypos != None:
                reefIndex = self.__reef_looking_index(aprilTagIndex)
                coralPositions.append([(xpos, ypos), reefIndex])

            # if all(closestToTop):
            #     if reefOrCoral in corals:
            #         ypos = 4
            # elif all(closestToBottom):
            #     if reefOrCoral in corals:
            #         ypos = 2
            # else:
            #     if reefOrCoral in corals:
            #         ypos = 3


        coralAndReefs.append(reefOrCoral)
            
        for position in coralPositions:
            xyPos, reefIndex = position[0], position[1]
            reefCopy[reefIndex[xyPos[0]]][xyPos[1]] = True

        return reefCopy
    
    def __reef_looking_index(self, aprilTagIndex: int) -> int:
        if self.team == "red":
            return constants.PhotonLibConstants.RED_APRIL_TAG_REEF_LOCATIONS[aprilTagIndex]
    
        elif self.team == "blue":
            return constants.PhotonLibConstants.BLUE_APRIL_TAG_REEF_LOCATIONS[aprilTagIndex]
        
    def __rect_touching_another_rect(self, rect1: list[TargetCorner], rect2: list[TargetCorner]):
        """
        If a rectangle (rect1) is touching another rectangle (rect2).

        Parameters:
            rect1 (list[TargetCorner]): List of target corners representing the bounding box around an object
            rect2 (list[TargetCorner]): List of target corners representing the bounding box around an object
        """

        def point_inside_rect(point: TargetCorner, rect: list[TargetCorner]):
            if rect[0].x < point.x and rect[2].x > point.x:
                if point.y > rect2[0].y and point.y < rect2[2].y:
                    return True

        pointsInRect = [True if point_inside_rect(point, rect2) else False for point in rect1]
        return True if any(pointsInRect) else False