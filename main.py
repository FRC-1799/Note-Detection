import time
import ntcore
import cv2
from constants import PhotonLibConstants
from classes import AprilTagCamera
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d
import keyboard


# Start NT server
inst = ntcore.NetworkTableInstance.getDefault()
inst.stopServer()
inst.setServerTeam(1799)
inst.startServer()

topic = inst.getStructTopic("RobotValues", Pose3d)
publisher = topic.getEntry("Pose3d")

# Create an instance of the AprilTag camera
grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)

def fetch_robot_position() -> Pose3d:
    """
    Calculates robot position and returns it
    
    Returns
    Pose3d[Transform3d, Rotation3d]: 3d position made up of the robot's position (x, y, z) and its rotation (roll, pitch, yaw)
    """

    position = grabAprilTagInformation.get_estimated_global_pose()
    return position

def main():
    running = True
    while running:
        # Get tags from the camera (or any other data you need)
        targets = grabAprilTagInformation.get_tags()

        if keyboard.is_pressed("q"):
            inst.stopServer()
            cv2.destroyAllWindows()
            break
        
        if targets:
            robot_position_process = multiprocessing.Process(target=fetch_robot_position)
            
            robot_position_process.start()
            robot_position_process.join()
            position = fetch_robot_position()
        
            if position:
                publisher.set(position.estimatedPose)

        

if __name__ == "__main__":
    main()
