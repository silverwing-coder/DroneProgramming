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

""" Define variables """
IMG_WIDTH, IMG_HEIGHT = 640, 480

""" Set drawing variables """
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

""" Create detector objects: FaceMesh and Hands """
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

""" Set start time for frame rate calculation """
TIME_START = time.time()

""" Set drawing spec of FaceMesh """
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

face_mesh = (mp_face_mesh.FaceMesh)(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

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
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    face_found = False
    if results.multi_face_landmarks:
      face_found = True
      for face_landmarks in results.multi_face_landmarks:
        face_found = True
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_CONTOURS,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_contours_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_IRISES,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_iris_connections_style())


    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

    # if(face_found):
    #     print(face_landmarks)

    TIME_STOP = time.time()
    fps = 1 / (TIME_STOP - TIME_START)
    TIME_START = TIME_STOP

    # Flip the image horizontally for a selfie-view display.
    cv2.putText(image, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow('MediaPipe Holistic', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()