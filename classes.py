from typing import Optional
from photonlibpy.estimatedRobotPose import EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
import robotpy_apriltag as apriltag
from wpimath.geometry import Transform3d, Pose2d, Pose3d, Translation3d
import constants
import math

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
        self.reef = constants.PhotonLibConstants.POSE3D_REEF_LOCATIONS

    def get_targets(self):
        """Gathers the targets located in the camera. In this case"""

        photonResult = self.camera.getLatestResult()
        targets = photonResult.getTargets()

        self.targets = []
        for target in targets:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > constants.PhotonLibConstants.POSE_AMBIGUITY_TOLERANCE:
                continue

            self.targets.append(target.bestCameraToTarget)
    
    def reefs_with_coral(self, robotPosition: Pose3d, ):
        coralPositions = []

        for coral in self.targets:

            # distanceToCoral = self.__area_percent_to_meters(coral.area)
            # coralFieldPosition = self.__find_coral_field_pose(distanceToCoral, robotPosition)
            # coralPositions.append(coralFieldPosition)

    def coral_field_position_math(self, robotPosition: Pose3d):
        coralPositions = []

        for coral in self.targets:
            distanceToCoral = self.__find_coral_pose_math(coral)
            coralFieldPosition = self.__find_coral_field_pose(distanceToCoral, robotPosition)
            coralPositions.append(coralFieldPosition)

        return coralPositions

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

    def __area_percent_to_meters(self, percentage: float) -> Pose3d:
        pass

    def __coral_xy_in_reef(self, coralPos: Pose3d) -> bool:
        pass
    
    def __find_coral_pose_math(self, coral: tuple[int, int]) -> Pose3d:
        coralX, coralY = coral[0], coral[1]

        y_distance = - self.__mount_height / math.tan(coralY * self._vert_angle_per_pixel - (self.__vert_fov_angle_rad/2) - self.__mount_angle_rad)
        y_dist_hyp = math.sqrt(self.__mount_height**2 + y_distance**2)
        x_distance = y_dist_hyp * math.tan(coralX * self._horiz_angle_per_pixel - (self.__horiz_fov_angle_rad/2))
        return (x_distance, y_distance)

    def __find_coral_field_pose(self, distanceToCoral: Pose3d, robotPosition: Pose3d) -> Translation3d:
        translationOfCoralPose = distanceToCoral.translation()
        translationOfRobotPose = robotPosition.translation()
        coralFieldPosition = translationOfCoralPose + translationOfRobotPose
        return coralFieldPosition