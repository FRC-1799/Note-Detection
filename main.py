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

def hitbox_maker():
    origin = Translation2d(FieldMirroringUtils.FIELD_WIDTH / 2, FieldMirroringUtils.FIELD_HEIGHT / 2);

    blueHitboxes, redHitboxes = [[] for _ in range(12)], [[] for _ in range(12)]

    branchesCenterPositionBlue = [
        addTranslation2ds(Translation2d(-4.810, 0.164), origin),  # A
        addTranslation2ds(Translation2d(-4.810, -0.164), origin),  # B
        addTranslation2ds(Translation2d(-4.690, -0.373), origin),  # C
        addTranslation2ds(Translation2d(-4.406, -0.538), origin),  # D
        addTranslation2ds(Translation2d(-4.164, -0.537), origin),  # E
        addTranslation2ds(Translation2d(-3.879, -0.374), origin),  # F
        addTranslation2ds(Translation2d(-3.759, -0.164), origin),  # G
        addTranslation2ds(Translation2d(-3.759, 0.164), origin),   # H
        addTranslation2ds(Translation2d(-3.880, 0.373), origin),  # I
        addTranslation2ds(Translation2d(-4.164, 0.538), origin),  # J
        addTranslation2ds(Translation2d(-4.405, 0.538), origin),  # K
        addTranslation2ds(Translation2d(-4.690, 0.374), origin)   # L
    ]

    branchesCenterPositionRed = [FieldMirroringUtils.flipTranslation2d(pos) for pos in branchesCenterPositionBlue]

    branchesFacingOutwardsBlue = [
        Rotation2d.fromDegrees(180), Rotation2d.fromDegrees(180), # A and B
        Rotation2d.fromDegrees(-120), Rotation2d.fromDegrees(-120), # C and D
        Rotation2d.fromDegrees(-60), Rotation2d.fromDegrees(-60), # E and F
        Rotation2d.fromDegrees(0), Rotation2d.fromDegrees(0), # G and H
        Rotation2d.fromDegrees(60), Rotation2d.fromDegrees(60), # I and J
        Rotation2d.fromDegrees(120), Rotation2d.fromDegrees(120), # K and L
    ]

    branchesFacingOutwardsRed = [FieldMirroringUtils.flipRotation2d(pos) for pos in branchesFacingOutwardsBlue]

    

    class ReefscapeReefBranch:
        """
        1 Branch of coral, facing a certain direction and at a certain height
        """
        def __init__(self, ideal_placement_position: Translation2d, facing_outwards: Rotation2d, height_meters: float, branch_inwards_direction_pitch_rad: float):
            self.ideal_coral_placement_pose = Pose3d(
                ideal_placement_position.x, ideal_placement_position.y, height_meters,
                Rotation3d(degreesToRadians(0), -branch_inwards_direction_pitch_rad, facing_outwards.rotateBy(Rotation2d(math.radians(180))).radians())
            )
            
            self.ideal_velocity_direction_pitch_to_score_rad = branch_inwards_direction_pitch_rad
            self.has_coral = False

    class ReefscapeReefTrough:
        """
        L1, with its outward facing direction and position
        """
        def __init__(self, center_position: Translation2d, outwards_facing: Rotation2d):
            #coral_rotation = Rotation3d(0, 0, addTranslation2ds(outwards_facing, Rotation2d(math.radians(90))))
            roll, pitch, yaw = degreesToRadians(0), degreesToRadians(0), outwards_facing.rotateBy(Rotation2d((math.radians(90)))).radians()
            coral_rotation = Rotation3d(roll, pitch, yaw)
            first_position = center_position, (Translation2d(0.08, outwards_facing))
            second_position = center_position, (Translation2d(-0.04, outwards_facing))
            self.first_placement_pose = Pose3d(first_position[1].X(), first_position[1].Y(), 0.48, coral_rotation)
            self.second_placement_pose = Pose3d(second_position[1].X(), second_position[1].Y(), 0.52, coral_rotation)
            self.ideal_coral_placement_pose = Translation3d(first_position[0].X(), first_position[0].Y(), 0.47)
            self.coral_count = 0

    class ReefscapeReefBranchesTower:
        """
        Whole branch of coral, with the center position of the field and the direction it's facing
        """
        def __init__(self, stick_center_position_on_field: Translation2d, facing_outwards: Rotation2d):

            # L1 trough, 15cm away from center
            self.L1 = ReefscapeReefTrough(
                addTranslation2ds(stick_center_position_on_field, Translation2d(0.15, facing_outwards.radians())),
                facing_outwards
            )

            # L2 stick, 20 cm away from center, 78cm above ground, 35 deg pitch
            self.L2 = ReefscapeReefBranch(
                addTranslation2ds(stick_center_position_on_field, Translation2d(0.2, facing_outwards.radians())),
                facing_outwards, 0.77, math.radians(-35)
            )

            # L3 stick, 20 cm away from center, 118cm above ground, 35 deg pitch
            self.L3 = ReefscapeReefBranch(
                addTranslation2ds(stick_center_position_on_field, Translation2d(0.2, facing_outwards.radians())),
                facing_outwards, 1.17, math.radians(-35)
            )

            # L4 stick, 30 cm away from center, 178cm above ground, vertical
            self.L4 = ReefscapeReefBranch(
                addTranslation2ds(stick_center_position_on_field, Translation2d(0.26, facing_outwards.radians())),
                facing_outwards, 1.78, math.radians(-90)
            )

        

    # Makes hitboxes out of the blue and branches and adds them to the list
    for i in range(12):
        branch = ReefscapeReefBranchesTower(branchesCenterPositionBlue[i], branchesFacingOutwardsBlue[i])
        branchL1Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L1.ideal_coral_placement_pose, CameraConstants.radius)
        branchL2Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
        branchL3Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
        branchL4Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
        blueHitboxes[i].extend([branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox])
        
        branch = ReefscapeReefBranchesTower(branchesCenterPositionRed[i], branchesFacingOutwardsRed[i])
        branchL1Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L1.ideal_coral_placement_pose, CameraConstants.radius)
        branchL2Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
        branchL3Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
        branchL4Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
        redHitboxes[i].extend([branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox])

    return blueHitboxes if team == "blue" else redHitboxes



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
        #print(levelSubscribers[0].get(defaultValue))
        reef = [booleanList.get(defaultValue) for booleanList in levelSubscribers]
    else:
        reef = [[False for _ in range(4)] for _ in range(12)]
    #print(reef)
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
        #print(reef)
        coralCamera.camera_loop(reef, hitboxes)
        for level in reef:
            for publisher in reefPublishers:
                publisher.set(level)
                published = True

if __name__ == "__main__":
    main()
