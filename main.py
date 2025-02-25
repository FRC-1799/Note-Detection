import multiprocessing.process
import time
import ntcore
import cv2
import wpimath
from ConstantsAndUtils.Constants import PhotonLibConstants, CoralAndAlgaeCameraConstants
from Classes.AprilTagCamera import *
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d, Translation2d, Rotation2d, Rotation3d
import keyboard
import Classes.CoralCamera as CoralCamera
from wpilib import DriverStation
from wpimath.units import degreesToRadians
from Classes.Hitbox import hitbox
from ConstantsAndUtils import FieldMirroringUtils
import subprocess
from pygrabber.dshow_graph import FilterGraph


team = "blue"



def grab_past_reef(reefSubscribers):
    defaultValue = [False for _ in range(12)]
    reef = [[] for _ in range(12)]
    for subscriber in reefSubscribers:
        reefLevelBools = subscriber.get(defaultValue)
        for i, level in enumerate(reef):
            level.append(reefLevelBools[i])
            
    return reef 

def coralCameraIndex() -> int:
    graph = FilterGraph()
    
    try:
        device = graph.get_input_devices().index(Constants.CoralAndAlgaeCameraConstants.CORAL_CAMERA_NAME)
    except ValueError:
        device = 0
        
    return device
    
def main():
    def fetchRobotPosition(queue: multiprocessing.Queue):
        """
        Calculates robot position and adds it to the queue
        """

        if aprilTagCameraFront.isConnected():
            aprilTagCameraConnectionPublisher.set(True)
            aprilTags = aprilTagCameraFront.get_tags()
            if aprilTags:
                robotPosition, timestamp = aprilTagCameraFront.get_estimated_global_pose()
                queue.put(robotPosition)
                if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
                    robotPosition=robotPosition.relativeTo(FieldMirroringUtils.FIELD_WIDTH, FieldMirroringUtils.FIELD_HEIGHT, 0, Rotation3d)

                if robotPosition:
                    robotPosePublisher.set(robotPosition.estimatedPose, int(timestamp))

                

    def fetchReefValues(queue: multiprocessing.Queue):
        """
        Finds coral and algae on the reef, and puts these values into the queue
        """

        if not queue.empty():
            robotPosition = queue.get()

            if coralCamera.camera.isOpened():
                reefCameraConnectionPublisher.set(True)
                reef = grab_past_reef(coralSubscribers)
                coralCamera.camera_loop(reef, "algea", coralHitboxes, "none",5, robotPosition)
                
                for level, publisher in enumerate(coralPublishers):
                    reefLevelBoolVals = []
                    for reefSection in reef:
                        reefLevelBoolVals.append(reefSection[level])
                    publisher.set(reefLevelBoolVals)
    
    # Start NT server
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.stopServer()
    inst.setServerTeam(1799)
    inst.startServer()

    # Reef Values
    reef = [[False for _ in range(4)] for _ in range(12)]
    algae = [[False for _ in range(2)] for _ in range(12)]
    defaultReef = [False for _ in range(4)]
    defaultAlgae = [False for _ in range(2)]
    algaeNotSeenCounterList = [[0 for _ in range(2)] for _ in range(12)]

    
    # Create an instance of the AprilTag camera
    aprilTagCameraFront = AprilTagCamera(PhotonLibConstants.APRIL_TAG_FRONT_CAMERA_NAME, PhotonLibConstants.ROBOT_TO_CAMERA_FRONT_TRANSFORMATION)
    aprilTagCameraBack = AprilTagCamera(PhotonLibConstants.APRIL_TAG_BACK_CAMERA_NAME, PhotonLibConstants.ROBOT_TO_CAMERA_BACK_TRANSFORMATION)

    # Grabs the Robot's topic and publisher
    robotPoseTopic = inst.getStructTopic("VisionRobotPose", Pose3d)
    robotPosePublisher = robotPoseTopic.publish()
    aprilTagCameraConnectionTopic = inst.getBooleanTopic("AprilTagCameraConnection")
    aprilTagCameraConnectionPublisher = aprilTagCameraConnectionTopic.publish()
    robotPosition = None

    # Reef Publishers and Subscribers
    reefTable = inst.getTable("ReefLocationTable")
    reefL1Topic = reefTable.getBooleanArrayTopic("ReefL1")
    reefL2Topic = reefTable.getBooleanArrayTopic("ReefL2")
    reefL3Topic = reefTable.getBooleanArrayTopic("ReefL3")
    reefL4Topic = reefTable.getBooleanArrayTopic("ReefL4")
    algae1Topic = reefTable.getBooleanArrayTopic("Algae1")
    algae2Topic = reefTable.getBooleanArrayTopic("Algae2")
    coralSubscribers = [reefL1Topic.subscribe(defaultReef), reefL2Topic.subscribe(defaultReef), reefL3Topic.subscribe(defaultReef), reefL4Topic.subscribe(defaultReef)] 
    coralPublishers = [reefL1Topic.publish(), reefL2Topic.publish(), reefL3Topic.publish(), reefL4Topic.publish()]
    algaeSubscribers = [algae1Topic.subscribe(defaultAlgae), algae2Topic.subscribe(defaultAlgae)]
    algaePublishers = [algae1Topic.publish(), algae2Topic.publish()]
    reefCameraConnectionTopic = inst.getBooleanTopic("ReefCameraConnection")
    reefCameraConnectionPublisher = reefCameraConnectionTopic.getEntry(True)


    # Reef Pose3D for debugging purposes
    reefPose3dTable = inst.getTable("reefPose3dTable")
    pose3dTableTopic = reefPose3dTable.getStructArrayTopic("pose", Pose3d)
    pose3dPublisher = pose3dTableTopic.publish()

    coralCamera = CoralCamera.CoralCamera(cameraIndex=coralCameraIndex())
    coralCameraOpened = coralCamera.camera.isOpened()
    reefCameraConnectionPublisher.set(False)
    
    coralHitboxes = hitbox.makeCoralHitboxes()
    algaeHitboxes = hitbox.makeAlgaeHitboxes()
    
    while True:
        # Get April Tags from the camera
        if keyboard.is_pressed("q"):
            inst.stopServer()
            cv2.destroyAllWindows()
            break

        if (aprilTagCameraFront.isConnected() or aprilTagCameraBack.isConnected()) and Constants.PhotonLibConstants.shouldTestAprilTags:
            aprilTagCameraConnectionPublisher.set(True)
            aprilTags = aprilTagCameraFront.get_tags()
            if aprilTags:
                robotPosition, timestamp = fetch_robot_position()
                if DriverStation.getAlliance == DriverStation.Alliance.kRed:
                    robotPosition = robotPosition.relativeTo(FieldMirroringUtils.FIELD_WIDTH, FieldMirroringUtils.FIELD_HEIGHT, 0, Rotation3d)


        robotPositionProcess = multiprocessing.Process(target=fetchRobotPosition, args=(queue,))
        reefValuesProcess = multiprocessing.Process(target=fetchReefValues, args=(queue,))

        robotPositionProcess.start()
        reefValuesProcess.start()

        if coralCamera.camera.isOpened() and robotPosition:
            reefCameraConnectionPublisher.set(True)
            reef = grab_past_reef(coralSubscribers)
            coralCamera.camera_loop(reef, algae, coralHitboxes, algaeHitboxes, algaeNotSeenCounterList, robotPosition)
            
            for level, publisher in enumerate(coralPublishers):
                reefLevelBoolVals = []
                for reefSection in reef:
                    reefLevelBoolVals.append(reefSection[level])
                publisher.set(reefLevelBoolVals) 
                             
    time.sleep(0.01)
            
if __name__ == "__main__":
    main()