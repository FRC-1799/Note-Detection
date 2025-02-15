from typing import Self
from wpimath.geometry import Pose3d, Rotation3d, Translation2d, Rotation2d, Translation3d
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

class CreateHitbox:
    def __init__(self, team: str = "blue"):
        self.self = self
        self.team = team

    def hitbox_maker(self):
        origin = Translation2d(FieldMirroringUtils.FIELD_WIDTH / 2, FieldMirroringUtils.FIELD_HEIGHT / 2);

        blueHitboxes, redHitboxes = [[] for _ in range(12)], [[] for _ in range(12)]

        # Translation2d of the reef's position on the field based on the origin
        branchesCenterPositionBlue = [
            Translation2d(-4.72, -3.05).__add__(origin),  # A
            addTranslation2ds(Translation2d(-4.72, -3.39), origin),  # B
            addTranslation2ds(Translation2d(-4.5, 1.5), origin),  # C
            addTranslation2ds(Translation2d(-4.2, 1.3), origin),  # D
            addTranslation2ds(Translation2d(-3.75, 0.25), origin),  # E
            addTranslation2ds(Translation2d(-3.5, 0.374), origin),  # F
            addTranslation2ds(Translation2d(-3.2, -0.24), origin),  # G
            addTranslation2ds(Translation2d(-3.2, 0.07), origin),   # H
            addTranslation2ds(Translation2d(-3.880, 0.373), origin),  # I
            addTranslation2ds(Translation2d(-4.164, 0.538), origin),  # J
            addTranslation2ds(Translation2d(-4.405, 0.538), origin),  # K
            addTranslation2ds(Translation2d(-4.690, 0.374), origin)   # L
        ]

        branchesCenterPositionRed = [FieldMirroringUtils.flipTranslation2d(pos) for pos in branchesCenterPositionBlue] # translates to red

        # Rotation2d of the rotation of each of the branches of coral
        branchesFacingOutwardsBlue = [
            Rotation2d.fromDegrees(180), Rotation2d.fromDegrees(180), # A and B
            Rotation2d.fromDegrees(-120), Rotation2d.fromDegrees(-120), # C and D
            Rotation2d.fromDegrees(-60), Rotation2d.fromDegrees(-60), # E and F
            Rotation2d.fromDegrees(0), Rotation2d.fromDegrees(0), # G and H
            Rotation2d.fromDegrees(60), Rotation2d.fromDegrees(60), # I and J
            Rotation2d.fromDegrees(120), Rotation2d.fromDegrees(120), # K and L
        ]

        branchesFacingOutwardsRed = [FieldMirroringUtils.flipRotation2d(pos) for pos in branchesFacingOutwardsBlue] # translates to red
        
        class ReefscapeReefBranch:
            """
            1 Branch of coral, facing a certain direction and at a certain height
            """
            def __init__(self, ideal_placement_position: Translation2d, facing_outwards: Rotation2d, height_meters: float, branch_inwards_direction_pitch_rad: float):
                self.ideal_coral_placement_pose = Pose3d(
                    ideal_placement_position.x, ideal_placement_position.y, height_meters,
                    Rotation3d(degreesToRadians(0), -branch_inwards_direction_pitch_rad, facing_outwards.rotateBy(Rotation2d(math.radians(180))).radians())
                )
                
                self.ideal_velocity_direction_pitch_to_score_rad = branch_inwards_direction_pitch_rad
                self.has_coral = False

        class ReefscapeReefTrough:
            """
            L1, with its outward facing direction and position
            """
            def __init__(self, center_position: Translation2d, outwards_facing: Rotation2d):
                #coral_rotation = Rotation3d(0, 0, addTranslation2ds(outwards_facing, Rotation2d(math.radians(90))))
                roll, pitch, yaw = degreesToRadians(0), degreesToRadians(0), outwards_facing.rotateBy(Rotation2d((math.radians(90)))).radians()
                coral_rotation = Rotation3d(roll, pitch, yaw)
                first_position = center_position, (Translation2d(0.08, outwards_facing))
                second_position = center_position, (Translation2d(-0.04, outwards_facing))
                self.first_placement_pose = Pose3d(first_position[1].X(), first_position[1].Y(), 0.48, coral_rotation)
                self.second_placement_pose = Pose3d(second_position[1].X(), second_position[1].Y(), 0.52, coral_rotation)
                self.ideal_coral_placement_pose = Translation3d(first_position[0].X(), first_position[0].Y(), 0.47)
                self.coral_count = 0

        class ReefscapeReefBranchesTower:
            """
            Whole branch of coral, with the center position of the field and the direction it's facing
            """
            def __init__(self, stick_center_position_on_field: Translation2d, facing_outwards: Rotation2d):

                # L1 trough, 15cm away from center
                self.L1 = ReefscapeReefTrough(
                    addTranslation2ds(stick_center_position_on_field, Translation2d(0.15, facing_outwards.radians())),
                    facing_outwards
                )

                # L2 stick, 20 cm away from center, 78cm above ground, 35 deg pitch
                self.L2 = ReefscapeReefBranch(
                    addTranslation2ds(stick_center_position_on_field, Translation2d(0.2, facing_outwards.radians())),
                    facing_outwards, 0.7, math.radians(-35)
                )

                # L3 stick, 20 cm away from center, 118cm above ground, 35 deg pitch
                self.L3 = ReefscapeReefBranch(
                    addTranslation2ds(stick_center_position_on_field, Translation2d(0.2, facing_outwards.radians())),
                    facing_outwards, 1.17, math.radians(-35)
                )

                # L4 stick, 30 cm away from center, 178cm above ground, vertical
                self.L4 = ReefscapeReefBranch(
                    addTranslation2ds(stick_center_position_on_field, Translation2d(0.26, facing_outwards.radians())),
                    facing_outwards, 1.78, math.radians(-90)
                )

            

        # Makes hitboxes out of the blue and branches and adds them to the list
        self.branchesList = []
        for i in range(12):
            branch = ReefscapeReefBranchesTower(branchesCenterPositionBlue[i], branchesFacingOutwardsBlue[i])
            self.branchesList.append(branch)
            branchL1Hitbox = hitbox.hitboxFromPose3d(branch.L1.first_placement_pose, CameraConstants.radius)
            branchL2Hitbox = hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
            branchL3Hitbox = hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
            branchL4Hitbox = hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
            blueHitboxes[i].extend([branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox])
            
            branch = ReefscapeReefBranchesTower(branchesCenterPositionRed[i], branchesFacingOutwardsRed[i])
            branchL1Hitbox = hitbox.hitboxFromPose3d(branch.L1.first_placement_pose, CameraConstants.radius)
            branchL2Hitbox = hitbox.hitboxFromPose3d(branch.L2.ideal_coral_placement_pose, CameraConstants.radius)
            branchL3Hitbox = hitbox.hitboxFromPose3d(branch.L3.ideal_coral_placement_pose, CameraConstants.radius)
            branchL4Hitbox = hitbox.hitboxFromPose3d(branch.L4.ideal_coral_placement_pose, CameraConstants.radius)
            redHitboxes[i].extend([branchL1Hitbox, branchL2Hitbox, branchL3Hitbox, branchL4Hitbox])

        return blueHitboxes if self.team == "blue" else redHitboxes
    
    def returnBranchesList(self):
        return self.branchesList