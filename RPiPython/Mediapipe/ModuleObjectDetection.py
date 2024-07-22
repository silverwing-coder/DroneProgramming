'''
Ver. Apr-2-24
Created by Sangmork Park (Virginia Military Institute)
'''

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MARGIN = 10
ROW_SIZE = 10
FONT_SIZE = 1.5
FONT_THICKNESS = 2;
TEXT_COLOR = (255, 0, 255)
BOX_COLOR = (0, 255, 0)

'''
@parameter: image, face landmarks
@return: annotated image
'''
def get_annotated_image_objects(image, detection_result) -> np.array:
    for detection in detection_result.detections:
        bbox = detection.bounding_box;
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x+bbox.width, bbox.origin_y+bbox.height
        cv2.rectangle(image, start_point, end_point, BOX_COLOR, 2)

        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + '(' + str(probability) +')'
        # print(result_text)
        text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE  + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)
    return image

'''
@parameter: image
@return: object detection results
'''
def get_object_detection_results(image):

    ''' image color channel affects detection performance
    convert color channel from GBR(Webcam) --> BGR (mediapipe) '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite')
    options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.5)

    ''' Load mediapipe-type input image '''
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    detector = vision.ObjectDetector.create_from_options(options)
    detection_result = detector.detect(mp_image)

    return detection_result