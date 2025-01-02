import time
from typing import Optional
import ntcore
from photonlibpy.estimatedRobotPose import EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
import robotpy_apriltag as apriltag
from wpimath.geometry import Transform3d, Pose2d
from constants import PhotonLibConstants

class GrabPhotonCameraInfo:
    def __init__(self, cameraName):
        self.cameraName = cameraName
        self.camera = PhotonCamera(self.cameraName)

        self.estimator = PhotonPoseEstimator(
            apriltag.loadAprilTagLayoutField(apriltag.AprilTagField.k2024Crescendo),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self.camera,
            PhotonLibConstants.ROBOT_TO_CAMERA_TRANSFORMATION,
        )

        self.estimator.multiTagFallbackStrategy = PoseStrategy.LOWEST_AMBIGUITY


    def get_estimated_global_pose(self) -> Optional[EstimatedRobotPose]:
        return self.estimator.update()


    def get_estimated_global_pose_2d(self) -> Optional[Pose2d]:
        result = self.estimator.update()
        if result:
            return result.estimatedPose.toPose2d()


    def get_tags(self) -> dict[int, Transform3d]:
        photon_result = self.camera.getLatestResult().getTargets()

        tags = {}
        for target in photon_result:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > 0.2:
                continue

            tags[target.fiducialId] = target.bestCameraToTarget

        return tags

photonInformation = GrabPhotonCameraInfo(PhotonLibConstants.CAMERA_NAME)

if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.startServer()
    print("NT server started!")

    while True:
        time.sleep(0.02)

        # Robot pose estimation
        position = photonInformation.get_estimated_global_pose()

        # Check if the pose is valid
        if position:
            
            print(f"X: {position.x}, Y: position = position.estimatedPose{position.y}, Z: {position.z}")