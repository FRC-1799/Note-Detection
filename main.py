import time
import os
os.path.join("lib/python3.12/site-packages/")
import ntcore

from constants import PhotonLibConstants
from classes import AprilTagCamera
import multiprocessing
from wpimath.geometry import Pose3d, Transform3d, Rotation3d

# Start NT server
inst = ntcore.NetworkTableInstance.getDefault()
inst.setServerTeam(1799)
inst.startServer()
table = inst.getTable("RobotValues")
pose_topic = table.getStructTopic("pose", Pose3d)



# Create an instance of the AprilTag camera
grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME)

# Function to process robot position
def fetch_robot_position() -> Pose3d:
    position = grabAprilTagInformation.get_estimated_global_pose()  # Get robot position
    return position

def publish_robot_position(robotPosition: Pose3d):
    # translation3D = [robotPosition.translation().x, robotPosition.translation().y, robotPosition.translation().z]
    # rotation3D =  [robotPosition.rotation().x, robotPosition.rotation().y, robotPosition.rotation().z]

    pose_topic.set(robotPosition)

    # table.putNumberArray("Robot Location", translation3D)
    # table.putNumberArray("Robot Rotation", rotation3D)

def main():
    while True:

        # Get tags from the camera (or any other data you need)
        targets = grabAprilTagInformation.get_tags()

        if targets:  # If there are targets detected
            # Create a new process to fetch the robot position

            start_time = time.time()

            robot_position_process = multiprocessing.Process(target=fetch_robot_position)
            
            robot_position_process.start()
            robot_position_process.join()
            position = fetch_robot_position()

            end_time = time.time()
            duration = end_time - start_time

            print(f"Process took {duration:.2f} seconds.")
            
            # Check if the pose is valid
            if position:
                publish_robot_position(position.estimatedPose)

if __name__ == "__main__":
    main()
