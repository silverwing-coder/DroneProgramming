"""
Edited by Sangmork Park, Jan-2023
Filename: ControlMain.py
Import: FunctionModules.py, DrawingModule.py

This is a code for testing controlling Tello drone with face and hand gesture
Operations
1. Extract face landmarks and draw on an image
2. Extract hands landmarks and draw on an image
3. Get face data (left-upper-corner, center-point, right-lower-corner)
4. Tello movement control
    4-1. By face (control distance and keep face centered)
    4-2. By hand (control maneuver by hand gesture)
"""

import cv2
import mediapipe as mp
import time
import pickle

from djitellopy import Tello

import FunctionModule as fm
import DrawingModule as dm
from google.protobuf.json_format import MessageToDict

""" Define global variables """
# IMG_SIZE = [640, 480]    # image window width and height
FACE_MODE_DISTANCE_RANGE = [15000, 30000]
HAND_MODE_DISTANCE_RANGE = [5000, 8000]

""" Default mode: face mode"""
FACE_MODE, HAND_MODE = True, False

""" This function make a drone keep distance from target focusing on the target (face) """
def executeFaceMode(image, face_points, lms_left, lms_right, bounding_box):
    face_mode, hand_mode = True, False

    cv2.putText(image, 'FACE MODE', (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    control_data = fm.getMovementControls(face_points, (image.shape[1], image.shape[0]),
                                          FACE_MODE_DISTANCE_RANGE)
    drone.send_rc_control(control_data[0], control_data[1], control_data[2], control_data[3])
    # print(control_data)

    lhands_in_box = fm.checkHandInBox(lms_left, bounding_box, image.shape)
    rhands_in_box = fm.checkHandInBox(lms_right, bounding_box, image.shape)
    # print(lhands_in_lb_box and rhands_in_rb_box)

    lthumb_up = fm.checkThumbUp(lms_left)
    rthumb_up = fm.checkThumbUp(lms_right)

    """ if both hands are in bounding boxes and two thumbs up, change mode from FACE to HAND """
    if (lhands_in_box and rhands_in_box and lthumb_up and rthumb_up):
        face_mode = False
        hand_mode = True
    # print(lthumb_up and lthumb_up)

    return face_mode, hand_mode


""" This function make a drone keep distance from target focusing on the target, and
    controls the drone with hand gestures  """
def executeHandMode(image, face_points, lms_left, lms_right, bounding_box):
    face_mode, hand_mode = False, True
    cv2.putText(image, 'HAND MODE', (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    control_data = fm.getMovementControls(face_points, (image.shape[1], image.shape[0]),
                                          HAND_MODE_DISTANCE_RANGE)
    drone.send_rc_control(control_data[0], control_data[1], control_data[2], control_data[3])
    # print(control_data)

    lhands_in_box = fm.checkHandInBox(lms_left, bounding_box, image.shape)
    rhands_in_box = fm.checkHandInBox(lms_right, bounding_box, image.shape)
    # print(lhands_in_lb_box and rhands_in_rb_box)

    # lthumb_up = fm.checkThumbUp(lms_left)
    # rthumb_up = fm.checkThumbUp(lms_right)

    lthumb_dn = fm.checkThumbDown(lms_left)
    rthumb_dn = fm.checkThumbDown(lms_right)

    """ if both hands are in bounding box and two thumbs down, land and exit program """
    if (lhands_in_box and rhands_in_box and lthumb_dn and rthumb_dn):
        drone.land()
        # print("land")
        time.sleep(1)

        drone.streamoff()
        cv2.destroyAllWindows()
        exit(0)

    """ Upload machine learning model saved by from pickle library """
    ld_model = pickle.load(open('kncpickle_file', 'rb'))

    lhand_id = fm.getHandIndex(lms_left, ld_model)
    # if(not fm.checkThumbUp(lms_left)):
    #     print("lhand-", lhand_id)
    rhand_id = fm.getHandIndex(lms_right, ld_model)
    # if(not fm.checkThumbUp(lms_right)):
    #     print("rhand-", rhand_id)

    """ if both hands are in bounding box and two indexes = C1, change mode from HAND to FACE """
    if (lhands_in_box and rhands_in_box and lhand_id=="C1" and rhand_id == "C1"):
        face_mode = True
        hand_mode = False

    """ if right hand only in bounding box and right index = C2, flip right """
    if (not lhands_in_box and rhands_in_box and rhand_id == "C2"):
        drone.flip_left()
        # print("right flip")
        time.sleep(1)

    """ if left hand only in bounding box and left index = C2, flip left """
    if (lhands_in_box and not rhands_in_box and lhand_id == "C2"):
        drone.flip_right()
        # print("left flip")
        time.sleep(1)

    """ if right hand only in bounding box and right index = C5, flip back """
    if (not lhands_in_box and rhands_in_box and rhand_id == "C5"):
        drone.flip_back()
        # print("back flip")
        time.sleep(1)

    """ if left hand only in bounding box and left index = C5, flip forward """
    if (lhands_in_box and not rhands_in_box and lhand_id == "C5"):
        # drone.flip_forward()
        # print("forward flip")
        time.sleep(1)

    """ if right hand only in bounding box and right index = C4, flip back """
    if (not lhands_in_box and rhands_in_box and rhand_id == "C4"):
        drone.rotate_counter_clockwise(360)
        # print("rotate counter-clock wise")
        time.sleep(1)

    """ if left hand only in bounding box and left index = C4, flip left """
    if (lhands_in_box and not rhands_in_box and lhand_id == "C4"):
        drone.rotate_clockwise(360)
        # print("rotate clock wise")
        time.sleep(1)

    return face_mode, hand_mode


""" Create drawing object and style objects """
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

""" Set drawing spec of FaceMesh """
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

""" Create detector objects: FaceMesh and Hands """
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

""" Creates FaceMesh and Hands detector objects """
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

""" Set start time for frame rate calculation """
TIME_START = time.time()

""" Open video camera and capture image from computer """
# capture = cv2.VideoCapture(0)
# capture.set(3, IMG_SIZE[0]) # image width
# capture.set(4, IMG_SIZE[1]) # image_height

""" Create Tello drone object and initialize operation """
drone = Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
drone.takeoff()
# drone.move_up(50)

# while capture.isOpened():
while True:
    """ Use computer camera for image data input """
    # success, image = capture.read()
    # if not success:
    #   print("Ignoring empty camera frame.")
    #   break

    image = drone.get_frame_read().frame
    # cv2.resize(image, (IMG_SIZE[1], IMG_SIZE[0]))
    # print(image.shape)

    """ To improve performance, optionally mark the image as not writeable to pass by reference."""
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)

    results = face_mesh.process(image)
    # print(len(results.multi_face_landmarks[0].landmark))
    """
    results.multi_face_landmarks
    - type: list
    - number of elements (len(results.multi_face_landmarks) : 1 ( = landmark)
    - landmark: 478 vector points (x, y, z)    
    """

    """ Draw the face mesh annotations on the image."""
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    face_found = False
    if results.multi_face_landmarks:
        face_found = True
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                #     connections=mp_face_mesh.FACEMESH_CONTOURS,
                #     connections=mp_face_mesh.FACEMESH_IRISES,
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

    """ To improve performance, optionally mark the image as not writeable topass by reference."""
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    # print(results.multi_hand_landmarks)
    """
    results.multi_hand_landmarks
    - type: list
    - landmark: 21 vector points (x, y, z) in each hand
    - can access each hand with "results.multi_hand_landmarks[index]

    results.multi_handedness 
    - type: list of dictionary
    - can identify handedness by index or label
    # """

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
                    # cv2.circle(image, (int(lm_position.x * IMG_SIZE[0]), int(lm_position.y * IMG_SIZE[1])), 15, (255, 0, 0), cv2.FILLED)
            elif handedness == 1:
                for lm_id, lm_position in enumerate(hand_landmarks.landmark):
                    lms_right.append((lm_position.x, lm_position.y, lm_position.z))
                    # cv2.circle(image, (int(lm_position.x * IMG_SIZE[0]), int(lm_position.y * IMG_SIZE[1])), 15, (0, 255, 255), cv2.FILLED)

    """ ##### control implementation section ##### """

    """ get face data: [left-upper-corner, center-point, right-lower-corner] """
    """ if no face is in the image, rotate clockwise 60 degree """
    if (not face_found):
        drone.rotate_clockwise(60)
        time.sleep(1)

    if(face_found):
        face_points = fm.getFacePointCoordinates(face_landmarks)
        # print(face_points)
        # face_length = int((face_points[2][1] - face_points[0][1]) * image.shape[1])
        face_length = int((face_points[2][1] - face_points[0][1]) * image.shape[0])

        # lf_bounding_box = ((int(face_points[1][0] * image.shape[1]) - 250, int(face_points[1][1] * image.shape[0])),
        #                    (int(face_points[1][0] * image.shape[1]) - 100, int(face_points[1][1] * image.shape[0]) + 150))
        # rt_bounding_box = ((int(face_points[1][0] * image.shape[1]) + 100, int(face_points[1][1] * image.shape[0])),
        #                    (int(face_points[1][0] * image.shape[1]) + 250, int(face_points[1][1] * image.shape[0]) + 150))
        bounding_box = ((int(face_points[1][0] * image.shape[1]) - 200, int(face_points[1][1] * image.shape[0]) - 100),
                        (int(face_points[1][0] * image.shape[1]) + 200, int(face_points[1][1] * image.shape[0]) + 200))

        # face_bounding_box = ((int(face_points[1][0] * image.shape[1]) - 250, int(face_points[1][1] * image.shape[0]) - 300),
        #                     (int(face_points[1][0] * image.shape[1]) + 250, int(face_points[1][1] * image.shape[0]) + 150) + 200)
        """ Draw target objects on the image """
        dm.drawTarget(image, face_points, face_length)
        # dm.drawBoundingBox(image, face_points)
        dm.drawGestureBox(image, face_points)

    if (face_found and FACE_MODE):
        FACE_MODE, HAND_MODE = executeFaceMode(image, face_points, lms_left, lms_right, bounding_box)

    if (face_found and HAND_MODE):
        FACE_MODE, HAND_MODE = executeHandMode(image, face_points, lms_left, lms_right, bounding_box)

    # drone.send_rc_control(control_data[0], control_data[1], control_data[2], control_data[3])

    TIME_STOP = time.time()
    fps = 1 / (TIME_STOP - TIME_START)
    TIME_START = TIME_STOP

    cv2.putText(image, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
    cv2.imshow('TELLO CONTROL', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# capture.release()
drone.land()
drone.streamoff()
cv2.destroyAllWindows()