import time
import ntcore
import cv2
from constants import PhotonLibConstants
from classes import *
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d
import keyboard


# Start NT server
inst = ntcore.NetworkTableInstance.getDefault()
inst.stopServer()
inst.setServerTeam(1799)
inst.startServer()

robotPoseTopic = inst.getStructTopic("RobotValues", Pose3d)
robotPosePublisher = robotPoseTopic.getEntry("Pose3d")
reefTopic = inst.getBooleanArrayTopic("ReefValues", bool)
reefPublisher = reefTopic.getEntry("Reef")

team = str(input("Team: "))

# Create an instance of the AprilTag camera
grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)
coralCamera = CoralCamera(constants.PhotonLibConstants.CORAL_CAMERA_NAME, team)
reefCamera = CoralCamera(constants.PhotonLibConstants.REEF_CAMERA_NAME, team)
coralCalculator = CoralCalculator(team)

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
        aprilTags = grabAprilTagInformation.get_tags()
        corals = coralCamera.get_targets()
        reefs = reefCamera.get_targets()

        if keyboard.is_pressed("q"):
            inst.stopServer()
            cv2.destroyAllWindows()
            break

        if aprilTags:
            robot_position_process = multiprocessing.Process(target=fetch_robot_position)
            
            robot_position_process.start()
            robot_position_process.join()
            position = fetch_robot_position()
        
            if position:
                robotPosePublisher.set(position.estimatedPose)

        if (corals or reefs) and aprilTags:
            for tag in aprilTags:
                if tag.fiducialId in constants.PhotonLibConstants.RED_APRIL_TAG_REEF_LOCATIONS.keys():
                    filledReef = coralCalculator.reefs_with_coral(tag.fiducialId, reefs, corals)
                    reefPublisher.set(filledReef)
                    

            

        

if __name__ == "__main__":
    main()
