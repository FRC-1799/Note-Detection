from typing import Optional
from photonlibpy.estimatedRobotPose import EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
import robotpy_apriltag as apriltag
from wpimath.geometry import Transform3d, Pose2d
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

        photon_result = self.camera.getLatestResult().getTargets()
        tags = {}
        for target in photon_result:
            # Skip target if its pose is too ambiguous
            if target.poseAmbiguity > 0.2:
                continue

            tags[target.fiducialId] = target.bestCameraToTarget

        return tags

# class GrabPhotonCameraInfo:
#     """
#     Pulls camera information down from Network Tables.
#     """

#     def __init__(self, cameraName: str, cameraType: str = "Note"):
#         """
#         When initialized, a PhotonCamera will be created, along with a PhotonPoseEstimator if the camera being passed is supposed to detect April Tags.
        
#         Parameters: 
#         cameraName  (str): Name of a camera in String format. Used to find which camera is being used in Photon Vision. 
#         cameraType (str): Optional Parameter that is what the camera will be doing. If it is detecting April Tags, pass Pose in for it, and leave the parameter blank if it is detecting objects.
#         """

#         self.cameraName = cameraName
#         self.camera = PhotonCamera(self.cameraName)

#         if cameraType == "Pose":
#             self.estimator = PhotonPoseEstimator(
#                 apriltag.loadAprilTagLayoutField(apriltag.AprilTagField.k2024Crescendo),
#                 PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
#                 self.camera,
#                 constants.PhotonLibConstants.ROBOT_TO_CAMERA_TRANSFORMATION,
#             )

#             self.estimator.multiTagFallbackStrategy = PoseStrategy.LOWEST_AMBIGUITY

#     def get_estimated_global_pose(self) -> Optional[EstimatedRobotPose]:
#         return self.estimator.update()

#     def get_estimated_global_pose_2d(self) -> Optional[Pose2d]:
#         result = self.estimator.update()
#         if result:
#             return result.estimatedPose.toPose2d()


#     def get_tags(self) -> dict[int, Transform3d]:
#         """
#         Gets April Tags found in the camera and returns them with their id number and estimated location.

#         Returns:
#         Dictionary[integer, Transform3d]: The integer is the ID for the April Tag and the Transform3d is the position of the tag
#         """

#         photon_result = self.camera.getLatestResult().getTargets()
#         tags = {}
#         for target in photon_result:
#             # Skip target if its pose is too ambiguous
#             if target.poseAmbiguity > 0.2:
#                 continue

#             tags[target.fiducialId] = target.bestCameraToTarget

#         return tags
    
#     def get_closest_note(self) -> Optional[PhotonTrackedTarget]:
#         """
#         Gets the targets found in the camera and determines which note is the closest based on its area, and returns it.

#         Returns:
#         None (None): if there are no notes
#         Note Information (PhotonTrackedTarget): Information about the note (pitch, yaw, etc.)
#         """

#         targets = self.camera.getLatestResult().getTargets()

#         if not targets:
#             return

#         # The target with the highest area will be the NOTE closest to us
#         closest_target = targets[0]
#         for target in targets:
#             if target.area > closest_target.area:
#                 closest_target = target

#         return closest_target
 