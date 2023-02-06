"""
Edited by Sangmork Park, Jan-2023
Filename: DrawingModule.py

This is a code for supporting ControlMain.py
Draw objects (targets, bounding boxes, etc.) on the image
"""

import cv2


def drawTarget(image, face_points, face_length):

    """ Draw face-circle """
    cv2.circle(image,
               (int(face_points[1][0] * image.shape[1]), int(face_points[1][1] * image.shape[0])), int(face_length / 4),
               (0, 0, 255), 1)
    cv2.line(image,
             (int(face_points[1][0] * image.shape[1]), int(face_points[1][1] * image.shape[0]) - 20),
             (int(face_points[1][0] * image.shape[1]), int(face_points[1][1] * image.shape[0]) + 20),
             (0, 0, 255), 2)
    cv2.line(image,
             (int(face_points[1][0] * image.shape[1]) - 20, int(face_points[1][1] * image.shape[0])),
             (int(face_points[1][0] * image.shape[1]) + 20, int(face_points[1][1] * image.shape[0])),
             (0, 0, 255), 2)


def drawBoundingBox(image, face_points):
    """ Draw face-box """
    # cv2.rectangle(image,
    #              (int(face_points[0][0] * image.shape[1]), int(face_points[0][1] * image.shape[0])),
    #              (int(face_points[0][0] * image.shape[1]) + face_length, int(face_points[0][1] * image.shape[0]) + face_length),
    #              (0, 255, 0), 2)

    """ Draw left-hand_bounding-box """
    cv2.rectangle(image,
                  (int(face_points[1][0] * image.shape[1]) - 250, int(face_points[1][1] * image.shape[0])),
                  (int(face_points[1][0] * image.shape[1]) - 100, int(face_points[1][1] * image.shape[0]) + 150),
                  (0, 255, 0), 1)
    """ Draw right-hand_bounding-box """
    cv2.rectangle(image,
                  (int(face_points[1][0] * image.shape[1]) + 100, int(face_points[1][1] * image.shape[0])),
                  (int(face_points[1][0] * image.shape[1]) + 250, int(face_points[1][1] * image.shape[0]) + 150),
                  (0, 255, 0), 1)


def drawGestureBox(image, face_points):

    """ Draw face-box """
    cv2.rectangle(image,
                  (int(face_points[1][0] * image.shape[1]) - 250, int(face_points[1][1] * image.shape[0]) - 250),
                  (int(face_points[1][0] * image.shape[1]) + 250, int(face_points[1][1] * image.shape[0]) + 150),
                  (255, 255, 255), 1)


def drawHandLamdmarks(image, hand_lms):

    if len(hand_lms) > 5:
        # for lm in range(len(lms_left)):
        for i in range(5):
            cv2.circle(image, hand_lms[i], 15, (255, 0, 0), cv2.FILLED)
