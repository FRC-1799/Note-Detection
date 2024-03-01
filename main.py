from inference import get_roboflow_model
import supervision as sv
import cv2
import time
import poseEstimate

start = time.time()
# define the image url to use for inference
video = cv2.VideoCapture(1)

# load a pre-trained yolov8n model
model = get_roboflow_model(model_id="note-detection-frc-2024/4", api_key="Q9t3AxF6Ra8qoPV2RqeC")
imageNumber = 0

noteCenterXandY = []

note_estimator = poseEstimate.NotePoseEstimator()
note_estimator.camera_mount_height = 0.72
note_estimator.camera_mount_angle = 45

note_estimator.vertical_fov_angle = 45.5
note_estimator.vertical_pixels = 480
note_estimator.horizontal_fov_angle = 53.14
note_estimator.horizontal_pixels = 680

# Returns the detection of a note
def returnNote(imgNum):
    success, imgNum = video.read()
    jpgImage = cv2.imencode('.jpg', imgNum)[1].tobytes()
    results = model.infer(jpgImage)

    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
    return detections

# Annotates the note image, not needed
def boxAnnotator(detection, img):
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    annotated_image = bounding_box_annotator.annotate(
        scene=img, detections=detection)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detection)

# Checks if there is a note
def isNote(detections):
    for item in detections['class_name']:
        if item == 'note':
            return True
        else:
            return False

# Adds the center points of the note(s) to the list
def addCenterPoints(detections):
    global noteCenterXandY

    if isNote(detections):
        for item in detections['class_name']:
            centerXPoint = (detections.xyxy[0][2] - detections.xyxy[0][0]) + detections.xyxy[0][0]
            centerYPoint = (detections.xyxy[0][3] - detections.xyxy[0][1]) + detections.xyxy[0][1]
            centerPoint = (centerXPoint, centerYPoint)

            noteCenterXandY.append(centerPoint)



while True:
    imageNumber += 1

    detections = returnNote(imageNumber)
    addCenterPoints(detections)

    # Gets distance on ground from note (can change based on usage)
    for note in noteCenterXandY:
        note_estimator.get_camera_ray_to_ground(note[1])

    

