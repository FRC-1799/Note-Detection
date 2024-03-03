from inference import get_roboflow_model
import supervision as sv
import cv2
import time
from poseEstimate import NotePoseEstimator

start = time.time()
# define the image url to use for inference
video = cv2.VideoCapture(0)

# load a pre-trained yolov8n model
model = get_roboflow_model(model_id="note-detection-frc-2024/4", api_key="Q9t3AxF6Ra8qoPV2RqeC")
imageNumber = 0

noteCenterXandY = []

note_estimator = NotePoseEstimator()
note_estimator.camera_mount_height = 0.79
note_estimator.camera_mount_angle = 45

note_estimator.vertical_fov_angle = 27.0
note_estimator.vertical_pixels = 480
note_estimator.horizontal_fov_angle = 39.6
note_estimator.horizontal_pixels = 640
    
# Returns the detection of a note
def returnNote(imgNum):
    success, imgNum = video.read()
    if success:
        jpgImage = cv2.imencode('.jpg', imgNum)[1].tobytes()
        results = model.infer(jpgImage)

        detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
        return detections
    else:
        return "Frame Not Captured!"

# Checks if there is a note
def isNote(detections):
    try:
        return detections['class_name'] != None
    except:
        return True

# Adds the center points of the note(s) to the list
def addCenterPoints(detections):
    global noteCenterXandY

    if isNote(detections):
        for item in detections['class_name']:
            centerXPoint = (detections.xyxy[0][2] - detections.xyxy[0][0]) + detections.xyxy[0][0]
            centerYPoint = (detections.xyxy[0][3] - detections.xyxy[0][1]) + detections.xyxy[0][1]

            noteCenterXandY.append((centerXPoint, centerYPoint))

# Main functionality of the program
def noteInCamera(detections):
    if detections == "Frame Not Captured!":
        print(detections)
    else:
        addCenterPoints(detections)
        
        # Gets (x,y) position of the note based on the camera
        if isNote(detections):
            for note in noteCenterXandY:
                print(note_estimator.get_x_y_distance_from_pixels(note[0], note[1]))


while True:
    imageNumber += 1

    detections = returnNote(imageNumber)
    noteInCamera(detections)