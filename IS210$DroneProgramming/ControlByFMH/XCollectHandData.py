"""
Edited by Sangmork Park, Jan-2023
Filename: TestFacemeshAndHands.py
This is a code for testing FaceMesh and Hands Tracking functions with an image (captured from a video clip)
Operations
1. Extract face landmarks and draw on an image
2. Extract hands landmarks and draw on an image
"""

import cv2
import mediapipe as mp
import time

import math
import numpy as np

from google.protobuf.json_format import MessageToDict

import pickle

""" Define variables """
IMG_WIDTH, IMG_HEIGHT = 640, 480

""" Set drawing variables """
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

""" Create detector objects: FaceMesh and Hands """
# mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

""" Set start time for frame rate calculation """
TIME_START = time.time()

""" Set drawing spec of FaceMesh """
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#
# dfile = open("dtsc.csv", 'a')
# dfile.write("lm2, lm3, lm4, lm5, lm6, lm7, lm8, lm9, lm10, lm11, lm12, lm13, lm14, lm15, lm16, lm17, lm18, lm19, lm20")
# save_count = 0;
while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)

    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    lms_left, lms_right = [], []

    """ hand_id identifies a hand in multi hands case """
    hand_id = 0;
    if results.multi_handedness:
        for hand_handedness in enumerate(results.multi_handedness):

            """ left_hand : handedness = 0,  right_hand : handedness = 1 """
            handedness = MessageToDict(hand_handedness[1])['classification'][0]['index']
            # handedness = MessageToDict(hand_handedness[1])['classification'][0]['label']

            hand_landmarks = results.multi_hand_landmarks[hand_id]
            hand_id += 1
            # print(hand_landmarks.landmark)
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            if handedness == 0:
                for lm_id, lm_position in enumerate(hand_landmarks.landmark):
                    # lms_left.append((int(lm_position.x * image.shape[1]), int(lm_position.y * image.shape[0])))
                    lms_left.append((lm_position.x, lm_position.y, lm_position.z))
                    # print("left added")
                    # cv2.circle(image, (int(lm_position.x * IMG_SIZE[0]), int(lm_position.y * IMG_SIZE[1])), 15, (255, 0, 0), cv2.FILLED)
            elif handedness == 1:
                for lm_id, lm_position in enumerate(hand_landmarks.landmark):
                    # lms_right.append((int(lm_position.x * image.shape[1]), int(lm_position.y * image.shape[0])))
                    lms_right.append((lm_position.x, lm_position.y, lm_position.z))
                    # print("right added")
                    # cv2.circle(image, (int(lm_position.x * IMG_SIZE[0]), int(lm_position.y * IMG_SIZE[1])), 15, (0, 255, 255), cv2.FILLED)


    # if cv2.waitKey(1) == ord('s'):
    #     save_count += 1
    #     print(save_count, " save")
    #     dfile.write('\n')
    #     origin = np.array(lms_left[0])
    #     origin_dist = math.dist(origin, np.array(lms_left[5]))
    #     for lm in lms_left[2:]:
    #         dist = math.dist(origin, np.array(lm))
    #         ratio = f'{dist/origin_dist:10.4f}'
    #         # print(ratio)
    #         dfile.write(str(ratio))
    #         dfile.write(", ")
    #     if save_count == 20:
    #         break

    # if (len(lms_left) > 0):
    #
    #     ftr = []
    #     origin = np.array(lms_left[0])
    #     origin_dist = math.dist(origin, np.array(lms_left[5]))
    #     for i in range(5):
    #         for j in range(2, 5):
    #             # print(i*4 + j)
    #             lm = lms_left[i*4 + j]
    #             dist = math.dist(origin, np.array(lm))
    #             ratio = f'{dist/origin_dist:10.4f}'
    #             ftr.append(float(ratio))
    #
    #     # print(ftr)
    #     data = [ftr]
    #     ld_model = pickle.load(open('kncpickle_file', 'rb'))
    #     result = ld_model.predict(data)
    #     print(result)

    TIME_STOP = time.time()
    fps = 1 / (TIME_STOP - TIME_START)
    TIME_START = TIME_STOP

    # Flip the image horizontally for a selfie-view display.
    cv2.putText(image, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow('MediaPipe Hand', image)

    if cv2.waitKey(1) & 0xFF == 27:
      break

# dfile.close()
cap.release()
