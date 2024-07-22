'''
Ver. Apr-2-24
Created by Sangmork Park (Virginia Military Institute)
'''

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

'''
@parameter: image, hand landmarks
@return: annotated image
'''
def get_annotated_image_hands(image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style())

        '''Get the top left corner of the detected hand's bounding box.'''
        # height, width, _ = annotated_image.shape
        # x_coordinates = [landmark.x for landmark in hand_landmarks]
        # y_coordinates = [landmark.y for landmark in hand_landmarks]
        # text_x = int(min(x_coordinates) * width)
        # text_y = int(min(y_coordinates) * height) - MARGIN

        ''' Draw handedness (left or right hand) on the image.'''
        # cv2.putText(annotated_image, f"{handedness[0].category_name}",
        #             (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
        #             FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image

'''
@parameter: image
@return: hand detect results
IMAGE mode implementation 
'''
def get_hands_detection_results(image, detector):

    ''' image color channel affects detection performance
    convert color channel from GBR(Webcam) --> BGR (mediapipe) '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    # options = vision.HandLandmarkerOptions(base_options=base_options,
    #                                        num_hands=2)
    # detector = vision.HandLandmarker.create_from_options(options)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    ''' Load mediapipe-type input image '''
    detection_result = detector.detect(mp_image)

    return detection_result

    ''' VIDEO_STREAM mode implementation '''
#     BaseOptions = mp.tasks.BaseOptions
#     HandLandmarker = mp.tasks.vision.HandLandmarker
#     HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
#     HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
#     VisionRunningMode = mp.tasks.vision.RunningMode
#     options = HandLandmarkerOptions(
#         base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
#         running_mode=VisionRunningMode.LIVE_STREAM,
#         result_callback=print_result)
#
#     with HandLandmarker.create_from_options(options) as landmarker:
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
#         landmarker.detect_async(mp_image, 100)
#         # detection_result = landmarker.detect_for_video(mp_image, 10)
#
# def print_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#     print('hand landmarker result: {}'.format(result))