import time
import ntcore
import cv2
import wpimath
from constants import PhotonLibConstants, CameraConstants
from classes import *
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d, Translation2d, Rotation2d, Rotation3d
import keyboard
import FieldMirroringUtils
import hitbox
import camera
from ntcore import BooleanArraySubscriber
from wpimath.units import degreesToRadians


team = "blue"

def addTranslation2ds(translation1: Translation2d, translation2: Translation2d):
    return Translation2d(translation1.X() + translation2.X(), translation1.Y() + translation2.Y())





def fetch_robot_position() -> Pose3d:
    """
    Calculates robot position and returns it
    
    Returns
    Pose3d[Transform3d, Rotation3d]: 3d position made up of the robot's position (x, y, z) and its rotation (roll, pitch, yaw)
    """

    position, timestamp = grabAprilTagInformation.get_estimated_global_pose()
    return position, timestamp

def grab_past_reef(levelSubscribers: list[BooleanArraySubscriber], published: bool):
    if published:
        defaultValue = [False for _ in range(4)]
        reef = [booleanList.get(defaultValue) for booleanList in levelSubscribers]
    else:
        reef = [[False for _ in range(4)] for _ in range(12)]
    return reef

def main():
    # Start NT server
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.stopServer()
    inst.setServerTeam(1799)
    inst.startServer()

    # Reef Values
    reef = [[False for _ in range(4)] for _ in range(12)]
    defaultReef = [False for _ in range(12)]

    # Grabs each of the topics for Network Tables
    robotPoseTopic = inst.getStructTopic("RobotPose", Pose3d)
    robotPosePublisher = robotPoseTopic.getEntry("Pose3d")

    reefA = inst.getBooleanArrayTopic("ReefA")
    reefB = inst.getBooleanArrayTopic("ReefB")
    reefC = inst.getBooleanArrayTopic("ReefC")
    reefD = inst.getBooleanArrayTopic("ReefD")
    reefE = inst.getBooleanArrayTopic("ReefE")
    reefF = inst.getBooleanArrayTopic("ReefF")
    reefG = inst.getBooleanArrayTopic("ReefG")
    reefH = inst.getBooleanArrayTopic("ReefH")
    reefI = inst.getBooleanArrayTopic("ReefI")
    reefJ = inst.getBooleanArrayTopic("ReefJ")
    reefK = inst.getBooleanArrayTopic("ReefK")
    reefL = inst.getBooleanArrayTopic("ReefL")
    reefEntrysList = [reefA, reefB, reefC, reefD, reefE, reefF, reefG, reefH, reefI, reefJ, reefK, reefL]

    reefSubscribers = [level.subscribe(defaultReef) for level in reefEntrysList]
    reefPublishers = [level.publish() for level in reefEntrysList]

    team = "blue"

    # Create an instance of the AprilTag camera
    grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)
    coralCamera = camera.CoralCamera()
    coralCalculator = CoralCalculator(team)

    hitboxes = hitbox_maker()

    published = False

    running = True
    while running:
        # Get April Tags from the camera
        aprilTags = grabAprilTagInformation.get_tags()

        if keyboard.is_pressed("q"):
            inst.stopServer()
            cv2.destroyAllWindows()
            break

        if aprilTags:
            robot_position_process = multiprocessing.Process(target=fetch_robot_position)
            
            robot_position_process.start()
            robot_position_process.join()
            position, timestamp = fetch_robot_position()
        
            if position:
                robotPosePublisher.set(position.estimatedPose, timestamp)

        reef = grab_past_reef(reefSubscribers, published)
        coralCamera.camera_loop(reef, hitboxes)

        for level in reef:
            for publisher in reefPublishers:
                publisher.set(level)
                published = True

if __name__ == "__main__":
    main()
