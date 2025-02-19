from typing import Self
from wpimath.geometry import Pose3d, Rotation3d, Translation2d, Rotation2d, Translation3d, Transform3d
from wpimath.units import degreesToRadians
from ConstantsAndUtils import FieldMirroringUtils
from ConstantsAndUtils.Constants import CameraConstants
import math

def addTranslation2ds(translation1: Translation2d, translation2: Translation2d):
    return Translation2d(translation1.X() + translation2.X(), translation1.Y() + translation2.Y())

class hitbox:

    def __init__(self, x: float, y:float, z:float, r:float):
        self.x, self.y, self.z, self.r = x, y, z, r

    @staticmethod
    def hitboxFromPose3d(pose:Pose3d, r: float)->Self:
        return hitbox(pose.X(), pose.Y(), pose.Z(), r)
    

    def colideXYZ(self, pointOnRay: tuple[float, float, float])->bool:
        pointX, pointY, pointZ = pointOnRay
        return (pointX-self.x)**2 + (pointY-self.y)**2 + (pointZ-self.z)**2 <= self.r**2
    
    def colidePose3d(self, pose:Pose3d)->bool:
        pointLocation = (pose.X(), pose.Y(), pose.Z())
        return self.colideXYZ(pointLocation)
    
    def getPose(self)->Pose3d:
        return Pose3d(Translation3d(self.x, self.y, self.z), Rotation3d(0,0,0))
    
    @staticmethod
    def makeHitboxes():
        origin = Translation3d(FieldMirroringUtils.FIELD_WIDTH / 2, FieldMirroringUtils.FIELD_HEIGHT / 2, 0)

        blueHitboxes = [[None, None, None, None] for _ in range(12)]
        

        # Translation2d of the reef's position on the field based on the origin
        blueStarts = [
            Translation3d(x=3.550000, y=1.055000, z=0), 
            Translation3d(x=3.550000, y=0.715000, z=0), 
            Translation3d(x=3.770000, y=5.605000, z=0), 
            Translation3d(x=4.070000, y=5.405000, z=0), 
            Translation3d(x=4.520000, y=4.355000, z=0), 
            Translation3d(x=4.770000, y=4.479000, z=0), 
            Translation3d(x=5.070000, y=3.865000, z=0), 
            Translation3d(x=5.070000, y=4.175000, z=0), 
            Translation3d(x=4.820000, y=3.555000, z=0), 
            Translation3d(x=4.470000, y=3.705000, z=0), 
            Translation3d(x=4.120000, y=2.585000, z=0), 
            Translation3d(x=3.770000, y=2.415000, z=0)
        ]

        editTran=[
            Translation3d(0.15, 0, 0.5),
            Translation3d(0.2, 0, 0.78),
            Translation3d(0.2, 0, 1.18),
            Translation3d(0.3, 0, 178),
        ]

        for i in range(12):
            for j in range(4):
                blueHitboxes[i][j] = hitbox.hitboxFromPose3d(Pose3d(origin, Rotation3d())
                    .transformBy(Transform3d(editTran[j], Rotation3d())).transformBy(Transform3d(blueStarts[i],Rotation3d())), CameraConstants.radius)
            
        return blueHitboxes
    
    @staticmethod
    def makeAlgaeHitboxes():

        blueHitboxes = [[] for _ in range(12)]



# class CreateHitbox:
#     def __init__(self, team: str = "blue"):
#         self.self = self
#         self.team = team

#     def coralHitboxMaker(self):





        
#         class ReefscapeReefBranch:
#             """
#             1 Branch of coral, facing a certain direction and at a certain height
#             """
#             def __init__(self, ideal_placement_position: Translation2d, facing_outwards: Rotation2d, height_meters: float, branch_inwards_direction_pitch_rad: float):
#                 self.ideal_coral_placement_pose = Pose3d(
#                     ideal_placement_position.x, ideal_placement_position.y, height_meters,
#                     Rotation3d(degreesToRadians(0), -branch_inwards_direction_pitch_rad, facing_outwards.rotateBy(Rotation2d(math.radians(180))).radians())
#                 )
                
#                 self.ideal_velocity_direction_pitch_to_score_rad = branch_inwards_direction_pitch_rad
#                 self.has_coral = False

#         class ReefscapeReefTrough:
#             """
#             L1, with its outward facing direction and position
#             """
#             def __init__(self, center_position: Translation2d, outwards_facing: Rotation2d):
#                 roll, pitch, yaw = degreesToRadians(0), degreesToRadians(0), outwards_facing.rotateBy(Rotation2d((math.radians(90)))).radians()
#                 coral_rotation = Rotation3d(roll, pitch, yaw)
#                 first_position = center_position, (Translation2d(0.6, outwards_facing))
#                 second_position = center_position, (Translation2d(-0.04, outwards_facing))
#                 self.first_placement_pose = Pose3d(first_position[0].X(), first_position[0].Y(), 0.48, coral_rotation)
#                 self.second_placement_pose = Pose3d(second_position[0].X(), second_position[0].Y(), 0.52, coral_rotation)
#                 self.ideal_coral_placement_pose = Translation3d(first_position[0].X(), first_position[0].Y(), 0.47)
#                 self.coral_count = 0

#         class ReefscapeReefBranchesTower:
#             """
#             Whole branch of coral, with the center position of the field and the direction it's facing
#             """
#             def __init__(self, stick_center_position_on_field: Translation2d, facing_outwards: Rotation2d):

#                 # L1 trough, 15cm away from center
#                 self.L1 = ReefscapeReefTrough(
#                     addTranslation2ds(stick_center_position_on_field, Translation2d(0.15, facing_outwards.radians())),
#                     facing_outwards
#                 )

#                 # L2 stick, 20 cm away from center, 78cm above ground, 35 deg pitch
#                 self.L2 = ReefscapeReefBranch(
#                     addTranslation2ds(stick_center_position_on_field, Translation2d(0.2, facing_outwards.radians())),
#                     facing_outwards, 0.72, math.radians(-35)
#                 )

#                 # L3 stick, 20 cm away from center, 118cm above ground, 35 deg pitch
#                 self.L3 = ReefscapeReefBranch(
#                     addTranslation2ds(stick_center_position_on_field, Translation2d(0.2, facing_outwards.radians())),
#                     facing_outwards, 1.17, math.radians(-35)
#                 )

#                 # L4 stick, 30 cm away from center, 178cm above ground, vertical
#                 self.L4 = ReefscapeReefBranch(
#                     addTranslation2ds(stick_center_position_on_field, Translation2d(0.15, facing_outwards.radians())),
#                     facing_outwards, 1.78, math.radians(-90)
#                 )

            

#         # Makes hitboxes out of the blue and branches and adds them to the list
#         self.branchesList = []
#         for i in range(12):
#             branch = ReefscapeReefBranchesTower(self.branchesCenterPositionBlue[i], self.branchesFacingOutwardsBlue[i])
#             self.branchesList.append(branch)
#             branchL1Hitbox = hitbox.hitboxFromPose3d(branch.L1.first_placement_pose, CameraConstants.radius)
#             branchL2Hitbox = hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
#             branchL3Hitbox = hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
#             branchL4Hitbox = hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
#             blueHitboxes[i].extend([branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox])
            


#         return blueHitboxes if self.team == "blue" else redHitboxes 
    
#     def algaeHitboxMaker(self):
#         class L2Algae:
#             def __init__(self, center_position: Translation2d, outwards_facing: Rotation2d):
#                 roll, pitch, yaw = degreesToRadians(0), degreesToRadians(0), outwards_facing.rotateBy(Rotation2d((math.radians(90)))).radians()
#                 coral_rotation = Rotation3d(roll, pitch, yaw)
#                 first_position = center_position, (Translation2d(0.6, outwards_facing))
#                 self.first_placement_pose = Pose3d(first_position[0].X(), first_position[0].Y(), 0.81, coral_rotation)

#         class L3Algae:
#             def __init__(self, center_position: Translation2d, outwards_facing: Rotation2d):
#                 roll, pitch, yaw = degreesToRadians(0), degreesToRadians(0), outwards_facing.rotateBy(Rotation2d((math.radians(90)))).radians()
#                 coral_rotation = Rotation3d(roll, pitch, yaw)
#                 first_position = center_position, (Translation2d(0.6, outwards_facing))
#                 self.first_placement_pose = Pose3d(first_position[0].X(), first_position[0].Y(), 1.21, coral_rotation)

#         class AlgaeTower:
#             """
#             The L2 and L3 algaes
#             """
#             def __init__(self, stick_center_position_on_field: Translation2d, facing_outwards: Rotation2d):

#                 # L2 position
#                 self.L2 = L2Algae(
#                     addTranslation2ds(stick_center_position_on_field, Translation2d(0.15, facing_outwards.radians())),
#                     facing_outwards
#                 )

#                 # L3 position
#                 self.L3 = L3Algae(
#                     addTranslation2ds(stick_center_position_on_field, Translation2d(0.15, facing_outwards.radians())),
#                     facing_outwards
#                 )

#        # for i in range(6):
#             #for i in self.branchesCenterPositionBlue:
#             #branch = AlgaeTower(self.branchesCenterPositionBlue[i], self.branchesFacingOutwardsBlue[i])
#             #self.branchesList.append(branch)
#             # branchL1Hitbox = hitbox.hitboxFromPose3d(branch.L1.first_placement_pose, CameraConstants.radius)
#             # branchL2Hitbox = hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
#             # branchL3Hitbox = hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
#             # branchL4Hitbox = hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
    
#     def returnBranchesList(self):
#         return self.branchesList