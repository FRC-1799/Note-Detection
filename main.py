from inference import get_roboflow_model
import supervision as sv
import math
import cv2
import time
from poseEstimate import NotePoseEstimator
from networktables import NetworkTables
import argparse

parser = argparse.ArgumentParser(description='Note Detection')
parser.add_argument('roboRioUrl')
args = parser.parse_args()

# As a client to connect to a robot
NetworkTables.initialize(server=args.roboRioUrl)
smartDashboard = NetworkTables.getTable('SmartDashboard')

start = time.time()
# define the image url to use for inference
video = cv2.VideoCapture(0)

# load a pre-trained yolov8n model
model = get_roboflow_model(model_id="note-detection-frc-2024/4", api_key="Q9t3AxF6Ra8qoPV2RqeC")

imageNumber = 0

noteCenterXandYandConfidence = []

note_estimator = NotePoseEstimator()
note_estimator.camera_mount_height = 0.79
note_estimator.camera_mount_angle = 45

note_estimator.vertical_fov_angle = 27.0
note_estimator.vertical_pixels = 480
note_estimator.horizontal_fov_angle = 39.6
note_estimator.horizontal_pixels = 640
    
# Returns the detection of a note
def return_note(imgNum):
    success, imgNum = video.read()
    if success:

        jpgImage = cv2.imencode('.jpg', imgNum)[1].tobytes()
        results = model.infer(jpgImage)

        detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
        return detections
    else:
        return "Frame Not Captured!"

# Checks if there is a note
def is_note(detections):
    try:
        return detections['class_name'].size > 0
    except:
        return True

# Adds the center points of the note(s) to the list
def add_center_points(detections):
    global noteCenterXandYandConfidence
    noteCenterXandYandConfidence = []

    if is_note(detections):
        for item in detections['class_name']:
            centerXPoint = (detections.xyxy[0][2] - detections.xyxy[0][0]) + detections.xyxy[0][0]
            centerYPoint = (detections.xyxy[0][3] - detections.xyxy[0][1]) + detections.xyxy[0][1]

            noteCenterXandYandConfidence.append((centerXPoint, centerYPoint, detections.confidence))

# Main functionality of the program
def note_in_camera(detections):
    add_center_points(detections)

    # Gets (x,y) position of the note based on the camera
    if is_note(detections):
        targetNote = max(noteCenterXandYandConfidence, key=lambda x: x[2][0]) #gets the note info with highest first confidence (I don't know why there's more than one confidence but there is.)
        print(str(note_estimator.get_x_y_distance_from_pixels(targetNote[0], targetNote[1])) + str(targetNote[2]))
        smartDashboard.putNumberArray("notePosition", toRobotPosit(note_estimator.get_x_y_distance_from_pixels(targetNote[0], targetNote[1])))
    else:
        print([0, 0])
        smartDashboard.putNumberArray("notePosition", [0, 0])

#expects the note offset where X is the forward distance and the robot position on the field
# returns a list of the note posit on the field
def toRobotPosit(coordinates):
    noteX = coordinates[1] #Assigns note-detection Y as X
    noteY = coordinates[0] #Assigns note-detection X as Y

    robotX = smartDashboard.getNumber("robotPositX", 1)
    robotY = smartDashboard.getNumber("robotPositY", 1)
    robotRotation = smartDashboard.getNumber("RobotRotation", 1)

    noteRotation=math.radians(robotRotation)+math.atan(noteY/noteX)
    noteDisance=math.sqrt(noteX**2+noteY**2)

    return [math.cos(noteRotation)*noteDisance+robotX, math.sin(noteRotation)*noteDisance+robotY]


while True:
    imageNumber += 1

    detections = return_note(imageNumber)
    note_in_camera(detections)