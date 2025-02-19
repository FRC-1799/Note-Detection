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
    defaultAlgae = [False for _ in range(2)]

    # Grabs each of the topics for Network Tables
    robotPoseTopic = inst.getStructTopic("visionRobotPose", Pose3d)
    robotPosePublisher = robotPoseTopic.getEntry(Pose3d())
    aprilTagCameraConnectionTopic = inst.getBooleanTopic("AprilTagCameraConnection")
    aprilTagCameraConnectionPublisher = aprilTagCameraConnectionTopic.getEntry(True)

    # Reef Publishers and Subscribers
    reefTable = inst.getTable("CoralLocations")
    reefL1Topic = reefTable.getBooleanArrayTopic("ReefL1")
    reefL2Topic = reefTable.getBooleanArrayTopic("ReefL2")
    reefL3Topic = reefTable.getBooleanArrayTopic("ReefL3")
    reefL4Topic = reefTable.getBooleanArrayTopic("ReefL4")
    algae1Topic = reefTable.getBooleanArrayTopic("Algae1")
    algae2Topic = reefTable.getBooleanArrayTopic("Algae2")
    coralSubscribers = [reefL1Topic.subscribe(defaultReef), reefL2Topic.subscribe(defaultReef), reefL3Topic.subscribe(defaultReef), reefL4Topic.subscribe(defaultReef)] 
    coralPublishers = [reefL1Topic.publish(), reefL2Topic.publish(), reefL3Topic.publish(), reefL4Topic.publish()]
    algaeSubscribers = [algae1Topic.publish(), algae2Topic.publish()]
    algaePublishers = [algae1Topic.publish(), algae2Topic.publish()]
    reefCameraConnectionTopic = inst.getBooleanTopic("ReefCameraConnection")
    reefCameraConnectionPublisher = reefCameraConnectionTopic.getEntry(True)


    # Reef Pose3D for debugging purposes
    reefPose3dTable = inst.getTable("reefPose3dTable")
    pose3dTableTopic = reefPose3dTable.getStructArrayTopic("pose", Pose3d)
    pose3dPublisher = pose3dTableTopic.publish()

    # Create an instance of the AprilTag camera
    aprilTagCamera = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)
    aprilTagCameraOpened = aprilTagCamera.isConnected()
    aprilTagCameraConnectionPublisher.set(aprilTagCameraOpened)

    #hitboxMakerClass = CreateHitbox()
    hitboxes = hitbox.makeHitboxes()#hitboxMakerClass.coralHitboxMaker()
    hitboxAlgae = hitbox.makeAlgaeHitboxes()

    coralCamera = CoralCamera.CoralCamera()
    coralCameraOpened = coralCamera.camera.isOpened()
    reefCameraConnectionPublisher.set(coralCameraOpened)
    
    hitboxMakerClass = CreateHitbox()
    hitboxes = hitboxMakerClass.coralHitboxMaker()
    hitboxAlgae = hitboxMakerClass.algaeHitboxMaker()


    
    while True:
        # Get April Tags from the camera
        if keyboard.is_pressed("q"):
            inst.stopServer()
            cv2.destroyAllWindows()
            break
        
        if aprilTagCamera.isConnected():
            aprilTags = aprilTagCamera.get_tags()
            if aprilTags:
                robot_position_process = multiprocessing.Process(target=fetch_robot_position)
                robot_position_process.start()
                robot_position_process.join()
                position, timestamp = fetch_robot_position()
            
                if position:
                    robotPosePublisher.set(position.estimatedPose, timestamp)



        poseList =[]
        for pole in hitboxes:
           
            for pose in pole:
                poseList.append(pose.getPose())
            #poseList.extend([branch.L2.first_placement_pose, branch.L3.first_placement_pose])
        ahhhPublisher.set(poseList)
        
        for level, publisher in enumerate(reefPublishers):
            reefLevelBoolVals = []
            for reefSection in reef:
                reefLevelBoolVals.append(reefSection[level])
            publisher.set(reefLevelBoolVals)

        if coralCameraOpened:
            reef = grab_past_reef(coralSubscribers)
            coralCamera.camera_loop(reef, "algea", hitboxes, "none",5)

            branchList = hitboxMakerClass.returnBranchesList()
            poseList = []
            for branch in branchList:
                poseList.extend([branch.L1.first_placement_pose, branch.L2.ideal_coral_placement_pose, branch.L3.ideal_coral_placement_pose, branch.L4.ideal_coral_placement_pose])
                #poseList.extend([branch.L2.first_placement_pose, branch.L3.first_placement_pose])
            
            
            for level, publisher in enumerate(coralPublishers):
                reefLevelBoolVals = []
                for reefSection in reef:
                    reefLevelBoolVals.append(reefSection[level])
                publisher.set(reefLevelBoolVals)


            pose3dPublisher.set(poseList)
            

        

if __name__ == "__main__":
    main()
