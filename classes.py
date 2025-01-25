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
            constants.PhotonLibConstants.ROBOT_TO_CAMERA_TRANSFORMATION,
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
    def __init__(self, cameraName):
        self.cameraName = cameraName
        self.camera = PhotonCamera(self.cameraName)

    def get_targets(self):
        """
        Gathers the targets located in the camera. In this case
        """

        photonResult = self.camera.getLatestResult()
        targets = photonResult.getTargets()

        self.targets = []
        for target in targets:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > constants.PhotonLibConstants.POSE_AMBIGUITY_TOLERANCE:
                continue

            self.targets.append(target.bestCameraToTarget)
    
    def reefs_with_coral(self, robotPosition: Pose3d, reefs: list[TargetCorner], corals: list[TargetCorner], reef: list):
        reefCopy = reef
        sortedReefs = [] # highest -> lowest
        coralAndReefs = reefs + corals
        sortedReefLevels = []

        for reef in reefs:
            reefRect = reef.getMinAreaRectCorners()
            for sortedReef in sortedReefs:
                sortedReefRect = sortedReef.getMinAreaRectCorners()
                if sortedReefRect[2].y < reefRect[2].y:
                    sortedReefs.insert(sortedReefs.index(sortedReef), reefRect)
            
            # If the lowest sorted reef is still higher than the reef, appened said reef to the end of sortedReefs
            if sortedReefRect[2].y > reefRect[2].y:
                sortedReefs.append(reef)

        if len(coralAndReefs) == 6:
            xpos = None # 0 is left, 1 is right
            ypos = None # level 0 is acutally level 2, level 1 is level 3, and level 2 is L4
            for reefOrCoral in coralAndReefs:
                reefRect = reefOrCoral.getMinAreaRectCorners()
                if reefRect[0].x - constants.PhotonLibConstants.REEF_X_TOLERANCE < all([xVal[0].x for xVal in coralAndReefs]):
                    if reefOrCoral in corals:
                        xpos = 0
                elif reefRect[1].x + constants.PhotonLibConstants.REEF_X_TOLERANCE > all([xVal[1].x for xVal in coralAndReefs]):
                    if reefOrCoral in corals:
                        xpos = 1

                if reefRect[0].y - constants.PhotonLibConstants.REEF_Y_TOLERANCE < all([yVal[0].y for yVal in coralAndReefs]):
                    if reefOrCoral in corals:
                        ypos = 2
                elif reefRect[2].y + constants.PhotonLibConstants.REEF_Y_TOLERANCE > all([yVal[2].y for yVal in coralAndReefs]):
                    if reefOrCoral in corals:
                        ypos = 0
                else:
                    if reefOrCoral in corals:
                        ypos = 1

                if xpos != None and ypos != None:
                    return reef

                
                

                

                
        if len(self.targets) > 1:
            for coral in self.targets:
                for reef in sortedReefs:
                    coralRect, reefRect = coral.getMinAreaRectCorners(), reef.getMinAreaRectCorners()
                    coralOnReef = self.__rect_inside_another_rect(reefRect, coralRect) # might occur when the coral is on level 2 or 3
                    if coralOnReef:
                        reefIndex = self.__reef_looking_index()
                        

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
    
    def __reef_looking_index(self, aprilTagIndex: int, team: str = "red"):
        if team == "blue":
            return constants.PhotonLibConstants.BLUE_APRIL_TAG_REEF_LOCATIONS.index(aprilTagIndex)
        
        elif team == "red":
            return constants.PhotonLibConstants.RED_APRIL_TAG_REEF_LOCATIONS.index(aprilTagIndex)
        
f a rectangle (rect1) is inside of another rectangle (rect2).
        """

        def get_bounds(rect: list[TargetCorner]):
            xCoords = [corner.x for corner in rect]
            yCoords = [corner.y for corner in rect]
            return min(xCoords), max(xCoords), min(yCoords), max(yCoords)

        rect1_min_x, rect1_max_x, rect1_min_y, rect1_max_y = get_bounds(rect1)
        rect2_min_x, rect2_max_x, rect2_min_y, rect2_max_y = get_bounds(rect2)

        return (rect1_min_x >= rect2_min_x and rect1_max_x <= rect2_max_x and
                rect1_min_y >= rect2_min_y and rect1_max_y <= rect2_max_y)
