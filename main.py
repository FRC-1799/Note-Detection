# import a utility function for loading Roboflow models
import os
from inference import get_roboflow_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2
import time

start = time.time()
# define the image url to use for inference
video = cv2.VideoCapture(1)

# load a pre-trained yolov8n model
model = get_roboflow_model(model_id="note-detection-frc-2024/4", api_key="Q9t3AxF6Ra8qoPV2RqeC")
i = 0
while True:
    i+=1
    succses, img = video.read()
    #imgJpg = cv2.imwrite("frame%d.jpg" % i, img)
    jpgImage = cv2.imencode('.jpg', img)[1].tobytes()
    results = model.infer(jpgImage)
     
    # take images, put them into a folder, then delete them when done

    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

    # # create supervision annotators
    # bounding_box_annotator = sv.BoundingBoxAnnotator()
    # label_annotator = sv.LabelAnnotator()



    # # annotate the image with our inference results
    # annotated_image = bounding_box_annotator.annotate(
    #     scene=imgJpg, detections=detections)
    # annotated_image = label_annotator.annotate(
    #     scene=annotated_image, detections=detections)



    try:
        for item in detections['class_name']:
            if item == 'note':
                centerXPoint = (detections.xyxy[0][2] - detections.xyxy[0][0]) + detections.xyxy[0][0]
                centerYPoint = (detections.xyxy[0][3] - detections.xyxy[0][1]) + detections.xyxy[0][1]
                centerPoint = (centerXPoint, centerYPoint)

                print(detections.xyxy[0][2] - detections.xyxy[0][0])
    except:
        pass

    #os.remove(f"frame{i}.jpg")


