from wpimath.geometry import Transform3d, Rotation3d, Translation2d, Rotation2d, Pose3d

class PhotonLibConstants():
    APRIL_TAG_CAMERA_NAME = "ArducamAprilTag"
    CORAL_CAMERA_NAME = "ArducamCoral"
    REEF_CAMERA_NAME = "ArducamReef"
    ROBOT_TO_CAMERA_TRANSFORMATION = Transform3d(-0.3164, 0, 0.1472, Rotation3d(0, 45, 0)) # Placeholder, fix this when robot is cadded
    POSE_AMBIGUITY_TOLERANCE = 0
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
