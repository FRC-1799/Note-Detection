import time
from Classes import Hitbox
import ntcore
import cv2
import wpimath
from ConstantsAndUtils.Constants import PhotonLibConstants, CameraConstants
from Classes.AprilTagCamera import *
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d, Translation2d, Rotation2d, Rotation3d
import keyboard
import Classes.CoralCamera as CoralCamera
from ntcore import BooleanArraySubscriber
from wpimath.units import degreesToRadians
from Classes.Hitbox import hitbox
import subprocess



team = "blue"

def fetch_robot_position() -> Pose3d:
    """
    Calculates robot position and returns it
    
    Returns
    Pose3d[Transform3d, Rotation3d]: 3d position made up of the robot's position (x, y, z) and its rotation (roll, pitch, yaw)
    """

    position, timestamp = grabAprilTagInformation.get_estimated_global_pose()
    return position, timestamp

def grab_past_reef(reefSubscribers):
    defaultValue = [False for _ in range(12)]
    reef = [[] for _ in range(12)]
    for subscriber in reefSubscribers:
        reefLevelBools = subscriber.get(defaultValue)
        for i, level in enumerate(reef):
            level.append(reefLevelBools[i])
            
    return reef

def main():
    # Start NT server
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.stopServer()
    inst.setServerTeam(1799)
    inst.startServer()

    # Reef Values
    reef = [[False for _ in range(4)] for _ in range(12)]
    defaultReef = [False for _ in range(4)]

    # Grabs each of the topics for Network Tables
    robotPoseTopic = inst.getStructTopic("RobotPose", Pose3d)
    robotPosePublisher = robotPoseTopic.getEntry("Pose3d")

    reefTable = inst.getTable("CoralLocations")
    reefL1Topic = reefTable.getBooleanArrayTopic("ReefL1")
    reefL2Topic = reefTable.getBooleanArrayTopic("ReefL2")
    reefL3Topic = reefTable.getBooleanArrayTopic("ReefL3")
    reefL4Topic = reefTable.getBooleanArrayTopic("ReefL4")
    reefSubscribers = [reefL1Topic.subscribe(defaultReef), reefL2Topic.subscribe(defaultReef), reefL3Topic.subscribe(defaultReef), reefL4Topic.subscribe(defaultReef)]
    reefPublishers = [reefL1Topic.publish(), reefL2Topic.publish(), reefL3Topic.publish(), reefL4Topic.publish()]

    fuckyou = inst.getTable("reefPose3dTable")
    mommy = fuckyou.getStructArrayTopic("pose", Pose3d)
    ahhhPublisher = mommy.publish()

    team = "blue"

    # Create an instance of the AprilTag camera
    #grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)
    coralCamera = CoralCamera.CoralCamera()

    #hitboxMakerClass = CreateHitbox()
    hitboxes = hitbox.makeHitboxes()#hitboxMakerClass.coralHitboxMaker()
    hitboxAlgae = hitbox.makeAlgaeHitboxes()

#java -jar PhotonVisionJar/photonvision-v2024.3.1-linuxx64.jar
    running = True
    while running:
        # Get April Tags from the camera
        #aprilTags = grabAprilTagInformation.get_tags()

        if keyboard.is_pressed("q"):
            inst.stopServer()
            cv2.destroyAllWindows()
            break

        # if aprilTags:
        #     robot_position_process = multiprocessing.Process(target=fetch_robot_position)
            
        #     robot_position_process.start()
        #     robot_position_process.join()
        #     position, timestamp = fetch_robot_position()
        
        #     if position:
        #         robotPosePublisher.set(position.estimatedPose, timestamp)

        reef = grab_past_reef(reefSubscribers)
        coralCamera.camera_loop(reef, "algea", hitboxes, "none")

        poseList =[]
        for pose in hitboxes:
            poseList.extend(pose.getPose())
            #poseList.extend([branch.L2.first_placement_pose, branch.L3.first_placement_pose])
        ahhhPublisher.set(poseList)
        
        for level, publisher in enumerate(reefPublishers):
            reefLevelBoolVals = []
            for reefSection in reef:
                reefLevelBoolVals.append(reefSection[level])
            publisher.set(reefLevelBoolVals)

        ahhhPublisher.set(poseList)
            

        

if __name__ == "__main__":
    main()
