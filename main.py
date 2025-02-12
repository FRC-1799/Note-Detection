import time
import ntcore
import cv2
from constants import PhotonLibConstants, CameraConstants
from classes import *
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d, Translation2d, Rotation2d, Rotation3d
import keyboard
import FieldMirroringUtils
import hitbox
import camera


def hitbox_maker():
    origin = Translation2d(FieldMirroringUtils.FIELD_WIDTH / 2, FieldMirroringUtils.FIELD_HEIGHT / 2);

    blueHitboxes, redHitboxes = [[] for _ in range(12)], [[] for _ in range(12)]

    branchesCenterPositionBlue = [
        Translation2d(-4.810, 0.164).__add__(origin),  # A
        Translation2d(-4.810, -0.164).__add__(origin),  # B
        Translation2d(-4.690, -0.373).__add__(origin),  # C
        Translation2d(-4.406, -0.538).__add__(origin),  # D
        Translation2d(-4.164, -0.537).__add__(origin),  # E
        Translation2d(-3.879, -0.374).__add__(origin),  # F
        Translation2d(-3.759, -0.164).__add__(origin),  # G
        Translation2d(-3.759, 0.164).__add__(origin),   # H
        Translation2d(-3.880, 0.373).__add__(origin),  # I
        Translation2d(-4.164, 0.538).__add__(origin),  # J
        Translation2d(-4.405, 0.538).__add__(origin),  # K
        Translation2d(-4.690, 0.374).__add__(origin)   # L
    ]

    branchesCenterPositionRed = [FieldMirroringUtils.flip(pos) for pos in branchesCenterPositionBlue]

    branchesFacingOutwardsBlue = [
        Rotation2d.fromDegrees(180), Rotation2d.fromDegrees(180), # A and B
        Rotation2d.fromDegrees(-120), Rotation2d.fromDegrees(-120), # C and D
        Rotation2d.fromDegrees(-60), Rotation2d.fromDegrees(-60), # E and F
        Rotation2d.fromDegrees(0), Rotation2d.fromDegrees(0), # G and H
        Rotation2d.fromDegrees(60), Rotation2d.fromDegrees(60), # I and J
        Rotation2d.fromDegrees(120), Rotation2d.fromDegrees(120), # K and L
    ]

    branchesFacingOutwardsRed = [FieldMirroringUtils.flip(pos) for pos in branchesFacingOutwardsBlue]

    

    class ReefscapeReefBranch:
        """
        1 Branch of coral, facing a certain direction and at a certain height
        """
        def __init__(self, ideal_placement_position: Translation2d, facing_outwards: Rotation2d, height_meters: float, branch_inwards_direction_pitch_rad: float):
            self.ideal_coral_placement_pose = Pose3d(
                ideal_placement_position.x, ideal_placement_position.y, height_meters,
                Rotation3d(0, -branch_inwards_direction_pitch_rad, facing_outwards.__add__(Rotation2d(Rotation2d.k180deg)).radians)
            )
            self.ideal_velocity_direction_pitch_to_score_rad = branch_inwards_direction_pitch_rad
            self.has_coral = False

    class ReefscapeReefTrough:
        """
        L1, with its outward facing direction and position
        """
        def __init__(self, center_position: Translation2d, outwards_facing: Rotation2d):
            coral_rotation = Rotation3d(0, 0, outwards_facing.__add__(Rotation2d.kCCW_90deg).radians)
            first_position = center_position.__add__(Translation2d(0.08, outwards_facing))
            second_position = center_position.__add__(Translation2d(-0.04, outwards_facing))
            self.first_placement_pose = Pose3d(first_position.get_x(), first_position.get_y(), 0.48, coral_rotation)
            self.second_placement_pose = Pose3d(second_position.get_x(), second_position.get_y(), 0.52, coral_rotation)
            self.ideal_placement_position = Translation3d(center_position.get_x(), center_position.get_y(), 0.47)
            self.coral_count = 0

    class ReefscapeReefBranchesTower:
        """
        Whole branch of coral, with the center position of the field and the direction it's facing
        """
        def __init__(self, stick_center_position_on_field: Translation2d, facing_outwards: Rotation2d):

            # L1 trough, 15cm away from center
            self.L1 = ReefscapeReefTrough(
                stick_center_position_on_field.__add__(Translation2d(0.15, facing_outwards.radians)),
                facing_outwards
            )

            # L2 stick, 20 cm away from center, 78cm above ground, 35 deg pitch
            self.L2 = ReefscapeReefBranch(
                stick_center_position_on_field.__add__(Translation2d(0.2, facing_outwards.radians)),
                facing_outwards, 0.77, math.radians(-35)
            )

            # L3 stick, 20 cm away from center, 118cm above ground, 35 deg pitch
            self.L3 = ReefscapeReefBranch(
                stick_center_position_on_field.__add__(Translation2d(0.2, facing_outwards.radians)),
                facing_outwards, 1.17, math.radians(-35)
            )

            # L4 stick, 30 cm away from center, 178cm above ground, vertical
            self.L4 = ReefscapeReefBranch(
                stick_center_position_on_field.__add__(Translation2d(0.26, facing_outwards.radians)),
                facing_outwards, 1.78, math.radians(-90)
            )

    # Makes hitboxes out of the blue and branches and adds them to the list
    for i in range(12):
        branch = ReefscapeReefBranchesTower(branchesCenterPositionBlue[i], branchesFacingOutwardsBlue[i])
        branchL1Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L1.ideal_coral_placement_pose, CameraConstants.radius)
        branchL2Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
        branchL3Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
        branchL4Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
        blueHitboxes[i].append(branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox)
        
        branch = ReefscapeReefBranchesTower(branchesCenterPositionRed[i], branchesFacingOutwardsRed[i])
        branchL1Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L1.ideal_coral_placement_pose, CameraConstants.radius)
        branchL2Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
        branchL3Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
        branchL4Hitbox = hitbox.hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
        redHitboxes[i].append(branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox)

    return blueHitboxes if team == "blue" else redHitboxes



def fetch_robot_position() -> Pose3d:
    """
    Calculates robot position and returns it
    
    Returns
    Pose3d[Transform3d, Rotation3d]: 3d position made up of the robot's position (x, y, z) and its rotation (roll, pitch, yaw)
    """

    position = grabAprilTagInformation.get_estimated_global_pose()
    return position

def main():
    # Start NT server
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.stopServer()
    inst.setServerTeam(1799)
    inst.startServer()

    # Grabs each of the topics for Network Tables
    robotPoseTopic = inst.getStructTopic("RobotValues", Pose3d)
    robotPosePublisher = robotPoseTopic.getEntry("Pose3d")
    #reefTopic = inst.getBooleanArrayTopic("ReefValues", bool)

    team = str(input("Team: "))

    # Create an instance of the AprilTag camera
    grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)
    coralCamera = camera.CoralCamera()
    coralCalculator = CoralCalculator(team)

    hitboxes = hitbox_maker()

    # Reef Values
    reef = [[False for _ in range(4)] for _ in range(12)]

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
            position = fetch_robot_position()
        
            if position:
                robotPosePublisher.set(position.estimatedPose)

        coralCamera.camera_loop(reef, hitboxes)

if __name__ == "__main__":
    main()