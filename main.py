import time
import ntcore
from constants import PhotonLibConstants
print("before")
from classes import AprilTagCamera
print("after")
import multiprocessing

# Start NT server
inst = ntcore.NetworkTableInstance.getDefault()
inst.startServer()
print("NT server started!")

# Create an instance of the AprilTag camera
grabAprilTagInformation = AprilTagCamera(PhotonLibConstants.APRIL_TAG_CAMERA_NAME, "Pose")

# Function to process robot position
def fetch_robot_position():
    position = grabAprilTagInformation.get_estimated_global_pose()  # Get robot position
    return position

def main():
    while True:
        time.sleep(0.02)  # Wait for 20ms

        # Get tags from the camera (or any other data you need)
        targets = grabAprilTagInformation.get_tags()

        if targets:  # If there are targets detected
            # Create a new process to fetch the robot position
            robot_position_process = multiprocessing.Process(target=fetch_robot_position)
            
            robot_position_process.start()
            robot_position_process.join()
            position = fetch_robot_position()
            
            # Check if the pose is valid
            if position:
                print(f"X: {position.x}, Y: {position.y}, Z: {position.z}")
        else:
            print("No targets detected.")

if __name__ == "__main__":
    main()
