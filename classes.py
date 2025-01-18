from typing import Optional
from photonlibpy.estimatedRobotPose import EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
import robotpy_apriltag as apriltag
from wpimath.geometry import Transform3d, Pose2d,Pose3d
import constants

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
        photonResult = self.camera.getLatestResult()
        targets = photonResult.getTargets()

        self.corals = []
        for target in targets:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > 0.2:
                continue

            self.corals.append(target.bestCameraToTarget)
    
    def distance_to_robot(self) -> Pose3d:
        self.corals