from typing import Self
from wpimath.geometry import Pose3d, Rotation3d
class hitbox:

    def __init__(self, x: float, y:float, z:float, r:float):
        self.x, self.y, self.z, self.r = x, y, z, r

    @staticmethod
    def hitboxFromPose3d(pose:Pose3d, r: float)->Self:
        return hitbox(pose.X(), pose.Y(), pose.Z(), r)
    

    def colides(self, x:float, y:float, z:float)->bool:
        return (x-self.x)**2 + (y-self.y)**2 + (z-self.z)**2 <= self.r**2
    
    def colides(self, pose:Pose3d)->bool:
        return self.colides(pose.X(), pose.Y(), pose.Z())