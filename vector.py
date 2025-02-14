from wpimath.geometry import Pose3d, Rotation3d, Transform3d
import math
class vector:
    def __init__(self, cameraPosition: tuple[float, float, float], pitch:float, yaw: float, NumbersInRad=True):
        self.self = self
        cameraX, cameraY, cameraZ = cameraPosition

        if NumbersInRad:
            self.pose = Pose3d(cameraX, cameraY, cameraZ, Rotation3d(0, pitch, yaw))

        else:
            self.pose = Pose3d(cameraX, cameraY, cameraZ, Rotation3d(0, math.degrees(pitch), (math.degrees(yaw))))

    


    def getPoseAtStep(self, lenght:float)->Pose3d:
        """
        Returns the pose of this vector when extended to the given length
        """
        return self.pose.transformBy(Transform3d(lenght, 0, 0, Rotation3d()))
    
