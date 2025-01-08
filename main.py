import time
import ntcore
from constants import PhotonLibConstants
from classes import *


if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.startServer()
    print("NT server started!")

    grabAprilTagInformation = GrabPhotonCameraInfo(PhotonLibConstants.APRIL_TAG_CAMERA_NAME, "Pose")
    # grabNoteInformation = GrabPhotonCameraInfo(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)

    while True:
        time.sleep(0.02)

        targets = grabAprilTagInformation.get_tags()

        # Robot pose estimation
        position = grabAprilTagInformation.get_estimated_global_pose()

        # Check if the pose is valid
        if position:
            position = position.estimatedPose
            print(f"X: {position.x}, Y: position = position.estimatedPose{position.y}, Z: {position.z}")

        # note = grabNoteInformation.get_closest_note()
        # if note:
        #     transform = note.bestCameraToTarget
        #     print(f"dYaw: {note.yaw}")
        #     print(f"(feet) x: {transform.x_feet}, y: {transform.y_feet}, z: {transform.z_feet}")