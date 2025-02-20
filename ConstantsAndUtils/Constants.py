from wpimath.geometry import Transform3d, Rotation3d, Translation2d, Rotation2d, Pose3d
import math

class PhotonLibConstants:
    APRIL_TAG_CAMERA_NAME = "ArducamAprilTag2"
    CORAL_CAMERA_NAME = "ArducamCoral"
    REEF_CAMERA_NAME = "ArducamReef"
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

    reef = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],      
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],      
        [False, False, False, False],
        [False, False, False, False]
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
    ROBOT_TO_CAMERA_TRANSFORMATION = Transform3d(2.513, 3.997, 0.72, Rotation3d(0, 0, 0)) # Placeholder, fix this when robot is cadded
    cameraPosition = (2.513, 3.997, 0.72)
    vectorLengthToExtend = 30 # m?
    radius = 0.1524
    confidenceTolerance = 0.60
    algaeViewedTolerance = 100 # Times we can not see the algae before we mark it as false

