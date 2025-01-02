from wpimath.geometry import Transform3d, Rotation3d, Translation2d, Rotation2d

class PhotonLibConstants():
    APRIL_TAG_CAMERA_NAME = "USB_Camera"
    NOTE_CAMERA_NAME = "USB_Camera"
    ROBOT_TO_CAMERA_TRANSFORMATION = Transform3d(-0.3164, 0, 0.1472, Rotation3d(0, 45, 0)) # Placeholder, fix this when robot is cadded