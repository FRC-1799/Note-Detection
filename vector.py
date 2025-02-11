from wpimath.geometry import Pose3d, Rotation3d, Transform3d
import math
@DeprecationWarning
class vector:
    
    def __init__ (self, x: float, y:float, z:float, pitch:float, yaw: float, NumbersInRad=True):

        if NumbersInRad:
            self.pose = Pose3d(x, y, z, Rotation3d(0, pitch, yaw))

        else:
            self.pose = Pose3d(x, y, z, Rotation3d(0, math.degrees(pitch), (math.degrees(yaw))))

    def __init__(self, pose:Pose3d):
        self.pose=pose
    

    """
        returns the pose of this vector when extended to the given length
    """
    def getPoseAtStep(self, lenght:float)->Pose3d:
        return self.transformBy(Transform3d(lenght, 0, 0, Rotation3d()))
    
