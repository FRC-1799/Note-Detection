from wpimath.geometry import Pose3d, Rotation3d
import math
class vector:
    
    def __init__ (self, x: float, y:float, z:float, pitch:float, yaw: float, NumbersInRad=True):
        self.x, self.y, self.z = x, y, x
        self.pitch, self.yaw = pitch, yaw
        if NumbersInRad:
            self.xRat = math.sin(yaw)
            self.yRat = math.cos(yaw)
            self.zRat = math.tan(pitch)

        else:
            self.xRat = math.sin(math.degrees(yaw))
            self.yRat = math.cos(math.degrees(yaw))
            self.zRat = math.tan(math.degrees(pitch))


    """
        returns the pose of this vector when extended to the given length
    """
    def getPoseAtStep(self, lenght:float)->Pose3d:
        return Pose3d(lenght*self.xRat+self.x, lenght*self.yRat+self.y, lenght*self.zRat+self.z, Rotation3d())
    
