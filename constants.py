from wpimath.geometry import Transform3d, Rotation3d, Translation2d, Rotation2d, Pose3d

class PhotonLibConstants():
    APRIL_TAG_CAMERA_NAME = "Arducam1"
    NOTE_CAMERA_NAME = "USB_Camera"
    ROBOT_TO_CAMERA_TRANSFORMATION = Transform3d(-0.3164, 0, 0.1472, Rotation3d(0, 45, 0)) # Placeholder, fix this when robot is cadded
    POSE_AMBIGUITY_TOLERANCE = 0.2
    REEF_WIDTH = 0.25   
    REEF_HEIGHT = 0.25   
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
    POSE3D_REEF_CORAL_POSE = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]
