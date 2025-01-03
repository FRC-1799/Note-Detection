import time
from typing import Optional
import ntcore
from photonlibpy.estimatedRobotPose import EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
import robotpy_apriltag as apriltag
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpimath.geometry import Transform3d, Pose2d
from constants import PhotonLibConstants

class GrabPhotonCameraInfo:
    """
    Pulls camera information down from Network Tables.
    """

    def __init__(self, cameraName: str, cameraType: str = "Note"):
        self.cameraName = cameraName
        self.camera = PhotonCamera(self.cameraName)

        if cameraType == "Pose":
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
        """
        Gets April Tags found in the camera and returns them with their id number and estimated location.
        """

        photon_result = self.camera.getLatestResult().getTargets()
        tags = {}
        for target in photon_result:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > 0.2:
                continue

            tags[target.fiducialId] = target.bestCameraToTarget

        return tags
    
    def get_closest_note(self) -> Optional[PhotonTrackedTarget]:
        """
        Gets the targets found in the camera and determines which note is the closest based on its area, and returns it.
        """

        targets = self.camera.getLatestResult().getTargets()

        if not targets:
            return

        # The target with the highest area will be the NOTE closest to us
        closest_target = targets[0]
        for target in targets:
            if target.area > closest_target.area:
                closest_target = target

        return closest_target

if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.startServer()
    #sd = inst.getTable("SmartDashboard")
    print("NT server started!")

    grabAprilTagInformation = GrabPhotonCameraInfo(PhotonLibConstants.APRIL_TAG_CAMERA_NAME, "Pose")
    # grabNoteInformation = GrabPhotonCameraInfo(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)

    while True:
        time.sleep(0.02)

        targets = grabAprilTagInformation.get_tags()

        # Robot pose estimation
        position = grabAprilTagInformation.get_estimated_global_pose()
        print("hye", position)

        # Check if the pose is valid
        if position:
            position = position.estimatedPose
            print(f"X: {position.x}, Y: position = position.estimatedPose{position.y}, Z: {position.z}")
            #sd.putNumber("Robot Pose X", position.translation().x)
            #sd.putNumber("Robot Pose Y", position.translation().y)
            #sd.putNumber("Robot Pose Z", position.translation().z)

        # note = grabNoteInformation.get_closest_note()
        # if note:
        #     transform = note.bestCameraToTarget
        #     print(f"dYaw: {note.yaw}")
        #     print(f"(feet) x: {transform.x_feet}, y: {transform.y_feet}, z: {transform.z_feet}")