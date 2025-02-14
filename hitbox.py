from typing import Self
from wpimath.geometry import Pose3d, Rotation3d
class hitbox:

    def __init__(self, x: float, y:float, z:float, r:float):
        self.x, self.y, self.z, self.r = x, y, z, r

    @staticmethod
    def hitboxFromPose3d(pose:Pose3d, r: float)->Self:
        return hitbox(pose.X(), pose.Y(), pose.Z(), r)
    

    def colideXYZ(self, pointOnRay: tuple[float, float, float])->bool:
        pointX, pointY, pointZ = pointOnRay
        print(pointX, pointY, pointZ)
        return (pointX-self.x)**2 + (pointY-self.y)**2 + (pointZ-self.z)**2 <= self.r**2
    
    def colidePose3d(self, pose:Pose3d)->bool:
        pointLocation = (pose.X(), pose.Y(), pose.Z())
        return self.colideXYZ(pointLocation)