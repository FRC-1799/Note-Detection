from wpimath.geometry import Transform3d, Rotation3d, Translation2d, Rotation2d, Pose3d
import math

class PhotonLibConstants:
    APRIL_TAG_CAMERA_NAME = "ArducamAprilTag"
    CORAL_CAMERA_NAME = "ArducamCoral"
    REEF_CAMERA_NAME = "ArducamReef"
    ROBOT_TO_CAMERA_TRANSFORMATION = Transform3d(-0.3164, 0, 0.1472, Rotation3d(0, 45, 0)) # Placeholder, fix this when robot is cadded
    POSE_AMBIGUITY_TOLERANCE = 0.20
    REEF_WIDTH = 0.25
    REEF_HEIGHT = 0.25  
    REEF_X_TOLERANCE = 0.5
    REEF_Y_TOLERANCE = 1

    POSE3D_REEF_LOCATIONS = [
        [Pose3d(4.75, 3.25, 0.45, Rotation3d()), Pose3d(4.75, 3.25, 0.8, Rotation3d()), Pose3d(4.75, 3.25, 1.2, Rotation3d()), Pose3d(4.75, 3.25, 1.825498, Rotation3d())],
        [Pose3d(5, 3.4, 0.45, Rotation3d()), Pose3d(5, 3.4, 0.8, Rotation3d()), Pose3d(5, 3.4, 1.2, Rotation3d()), Pose3d(4, 3.4, 1.825498, Rotation3d())],
        [Pose3d(5.3, 3.8, 0.45, Rotation3d()), Pose3d(5.3, 3.8, 0.8, Rotation3d()), Pose3d(5.3, 3.8, 1.2, Rotation3d()), Pose3d(5.3, 3.8, 1.825498, Rotation3d())],
        [Pose3d(5.3, 4.1, 0.45, Rotation3d()), Pose3d(5.3, 4.1, 0.8, Rotation3d()), Pose3d(5.3, 4.1, 1.2, Rotation3d()), Pose3d(5.3, 4.1, 1.825498, Rotation3d())],
        [Pose3d(5, 4.6, 0.45, Rotation3d()), Pose3d(5, 4.6, 0.8, Rotation3d()), Pose3d(5, 4.6, 1.2, Rotation3d()), Pose3d(4, 4.6, 1.825498, Rotation3d())],
        [Pose3d(4.75, 4.8, 0.45, Rotation3d()), Pose3d(4.75, 4.8, 0.8, Rotation3d()), Pose3d(4.75, 4.8, 1.2, Rotation3d()), Pose3d(4.75, 4.8, 1.825498, Rotation3d())],
        [Pose3d(4.2, 4.8, 0.45, Rotation3d()), Pose3d(4.2, 4.8, 0.8, Rotation3d()), Pose3d(4.2, 4.8, 1.2, Rotation3d()), Pose3d(4.2, 4.8, 1.825498, Rotation3d())],
        [Pose3d(4, 4.6, 0.45, Rotation3d()), Pose3d(4, 4.6, 0.8, Rotation3d()), Pose3d(4, 4.6, 1.2, Rotation3d()), Pose3d(4, 4.6, 1.825498, Rotation3d())],
        [Pose3d(3.6, 4.1, 0.45, Rotation3d()), Pose3d(3.6, 4.1, 0.8, Rotation3d()), Pose3d(3.6, 4.1, 1.2, Rotation3d()), Pose3d(3.6, 4.1, 1.825498, Rotation3d())],
        [Pose3d(3.6, 3.8, 0.45, Rotation3d()), Pose3d(3.6, 3.8, 0.8, Rotation3d()), Pose3d(3.6, 3.8, 1.2, Rotation3d()), Pose3d(3.6, 3.8, 1.825498, Rotation3d())],
        [Pose3d(4, 3.4, 0.45, Rotation3d()), Pose3d(4, 3.4, 0.8, Rotation3d()), Pose3d(4, 3.4, 1.2, Rotation3d()), Pose3d(4, 3.4, 1.825498, Rotation3d())],
        [Pose3d(4.2, 3.25, 0.45, Rotation3d()), Pose3d(4.2, 3.25, 0.8, Rotation3d()), Pose3d(4.2, 3.25, 1.2, Rotation3d()), Pose3d(4.2, 3.25, 1.825498, Rotation3d())],
    ]

    

    RED_APRIL_TAG_REEF_LOCATIONS = {6: (0, 1), 7: (2, 3), 8: (4, 5), 9: (6, 7), 10: (8, 9), 11: (10, 11)}
    BLUE_APRIL_TAG_REEF_LOCATIONS = {17: (0, 1), 18: (2, 3), 19: (4, 5), 20: (6, 7), 21: (8, 9), 22: (10, 11)}

class CameraConstants:
    horizontalAngleRad = math.radians(70)
    verticalAngleRad = math.radians(70)
    horizontalPixels = 640
    verticalPixels = 384
    reefCameraHorizontalAnglePerPixel = horizontalAngleRad / horizontalPixels
    reefCameraVerticalAnglePerPixel = verticalAngleRad / verticalPixels

# Constants for field dimensions
FIELD_WIDTH = 10  # Example value, replace with actual
FIELD_HEIGHT = 10  # Example value, replace with actual

origin = Translation2d(FIELD_WIDTH / 2, FIELD_HEIGHT / 2)

branches_center_position_blue = [
    Translation2d(-4.810, 0.164).plus(origin),  # A
    Translation2d(-4.810, -0.164).plus(origin), # B
    Translation2d(-4.690, -0.373).plus(origin), # C
    Translation2d(-4.406, -0.538).plus(origin), # D
    Translation2d(-4.164, -0.537).plus(origin), # E
    Translation2d(-3.879, -0.374).plus(origin), # F
    Translation2d(-3.759, -0.164).plus(origin), # G
    Translation2d(-3.759, 0.164).plus(origin),  # H
    Translation2d(-3.880, 0.373).plus(origin),  # I
    Translation2d(-4.164, 0.538).plus(origin),  # J
    Translation2d(-4.405, 0.538).plus(origin),  # K
    Translation2d(-4.690, 0.374).plus(origin)   # L
]

class ReefscapeReefBranchesTower:
    def __init__(self, stick_center_position_on_field, facing_outwards):
        self.L1 = ReefscapeReefTrough(
            stick_center_position_on_field.plus(Translation2d(0.15, facing_outwards.radians)),
            facing_outwards
        )
        self.L2 = ReefscapeReefBranch(
            stick_center_position_on_field.plus(Translation2d(0.2, facing_outwards.radians)),
            facing_outwards,
            0.77,
            math.radians(-35)
        )
        self.L3 = ReefscapeReefBranch(
            stick_center_position_on_field.plus(Translation2d(0.2, facing_outwards.radians)),
            facing_outwards,
            1.17,
            math.radians(-35)
        )
        self.L4 = ReefscapeReefBranch(
            stick_center_position_on_field.plus(Translation2d(0.26, facing_outwards.radians)),
            facing_outwards,
            1.78,
            math.radians(-90)
        )

class ReefscapeReefBranch:
    def __init__(self, ideal_placement_position, facing_outwards, height_meters, branch_inwards_direction_pitch_rad):
        self.ideal_coral_placement_pose = Pose3d(
            ideal_placement_position.x,
            ideal_placement_position.y,
            height_meters,
            Rotation3d(
                0,
                -branch_inwards_direction_pitch_rad,
                facing_outwards.plus(Rotation2d(math.pi)).radians
            )
        )
        self.ideal_velocity_direction_pitch_to_score_rad = branch_inwards_direction_pitch_rad
        self.has_coral = False



	
