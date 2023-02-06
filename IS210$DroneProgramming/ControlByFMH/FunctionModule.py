"""
Edited by Sangmork Park, Jan-2023
Filename: FunctionModule.py

This is a code for supporting ControlMain.py
Define functions of data extraction and control information

"""
import numpy as np

""" This function returns three points of interest on a face
    - left-upper-corner, center-point, right-lower-corner """
def getFacePointCoordinates(face_lms):

    # print(face_lms.landmark)
    # print(len(face_lms.landmark))
    """
    left-end landmarks: 21, 162, 177
    upper-end landmarks: 67, 10, 297
    center-x landmarks: 0, 5, 9
    center-y landmarks: 50, 4, 280
    right-end landmarks: 251, 389, 401
    lower-end landmarks: 148, 152, 377
    """

    fb_minX = np.average([face_lms.landmark[21].x, face_lms.landmark[162].x, face_lms.landmark[177].x])
    fb_minY = np.average([face_lms.landmark[67].y, face_lms.landmark[10].y, face_lms.landmark[297].y])
    fb_centerX = np.average([face_lms.landmark[0].x, face_lms.landmark[5].x, face_lms.landmark[9].x])
    fb_centerY = np.average([face_lms.landmark[50].y, face_lms.landmark[4].y, face_lms.landmark[280].y])
    fb_maxX = np.average([face_lms.landmark[251].x, face_lms.landmark[389].x, face_lms.landmark[401].x])
    fb_maxY = np.average([face_lms.landmark[148].y, face_lms.landmark[152].y, face_lms.landmark[377].y])

    face_point_coordinates = [(fb_minX, fb_minY), (fb_centerX, fb_centerY), (fb_maxX, fb_maxY)]
    # print(face_point_coordinates)

    return face_point_coordinates


""" This function returns movement controls based on three face-point coordinates
    - left-right speed: difference between left-face-size and right-face-size
    - forward-back speed: difference between distance and distance range
    - up-down speed: difference between image-center-y point and face-center-y point
    - yaw speed: difference between image-center-x point and face-center-x point
"""
def getMovementControls(face_coordinates, img_size, dist_range):

    # face_center = face_coordinates[1]
    face_length = int((face_coordinates[2][1] - face_coordinates[0][1]) * img_size[1])

    face_size = face_length * face_length
    # print(face_size)

    lr_speed, fb_speed, ud_speed, yaw_speed = 0, 0, 0, 0

    """ Calculate left and right movement speed: left(-), right(+) 
        img_size[0] = width, img_size[1] = height   """
    lf_dist = abs(face_coordinates[1][0] - face_coordinates[0][0])
    rt_dist = abs(face_coordinates[2][0] - face_coordinates[1][0])
    lr_speed = (rt_dist - lf_dist) * img_size[0] * 0.1
    # print(lr_speed)

    """ Calculate back and forward movement speed: forward(+), backward(-) """
    if (face_size > dist_range[1]):
        fb_speed = (dist_range[1] - face_size) * 0.001
    elif (face_size < dist_range[0]):
        fb_speed = (dist_range[0] - face_size) * 0.005
    # print(fb_speed)

    """ Calculate up and down movement speed: up(+), down(-) """
    ud_speed = (img_size[1]/2 - face_coordinates[1][1] * img_size[1]) * 0.1
    # print(ud_speed)

    """ Calculate yaw movement speed: left(-), right(+) """
    yaw_speed = (img_size[0]/2 - face_coordinates[1][0] * img_size[0]) * 0.01
    # print(yaw_speed)

    return [int(lr_speed), int(fb_speed), int(ud_speed), int(yaw_speed)]

""" This function checks if a palm is in a bounding box.
    returns "True" if the palm is in the respective bounding box 
"""
def checkHandInBox(lms, b_box):

    """ if no hand landmarks, return False. """
    if(len(lms) < 1 ):
        return False

    palm_in_box = True

    """ palm landmarks index: 0, 1, 2, 5, 9, 13, 17 """
    palm_lms = [lms[0], lms[1], lms[2], lms[5], lms[9], lms[13], lms[17]]

    for lm in palm_lms:
        if (lm[0] < b_box[0][0]) or (lm[0] > b_box[1][0]) or (lm[1] < b_box[0][1]) or (lm[1] > b_box[1][1]):
            # return False
            palm_in_box = False
            break

    return palm_in_box


""" This function checks if thumb is up.
    returns "True" if thumb is up 
"""
def checkThumbUp(lms):

    """ if no hand landmarks, return False. """
    if(len(lms) < 1 ):
        return False

    thumb_up = True

    """ thumb check landmarks index: 3, 4 """
    if lms[3][1] < lms[4][1]:
        return False

    for lm in lms[5:]:
        if (lm[1] < lms[4][1]):
            thumb_up = False
            break

    return thumb_up


""" This function checks if thumb is down.
    returns "True" if thumb is down
"""
def checkThumbDown(lms):

    """ if no hand landmarks, return False. """
    if(len(lms) < 1 ):
        return False

    thumb_down = True

    """ thumb check landmarks index: 3, 4 """
    if lms[4][1] < lms[3][1]:
        return False

    for lm in lms[5:]:
        if (lm[1] > lms[4][1]):
            thumb_down = False
            break

    return thumb_down


""" This function checks if index finger is up.
    returns "True" if index finger is up 
"""
def checkIndexUp(lms):

    """ if no hand landmarks, return False. """
    if(len(lms) < 1 ):
        return False

    index_up = True

    """ index check landmarks index: 6, 7, 8 """
    if (lms[7][1] < lms[8][1]) or (lms[6][1] < lms[7][1]) :
        return False

    for lm in lms[9:]:
        if (lm[1] < lms[8][1]):
            index_up = False
            break

    return index_up



""" This function checks if index finger is down.
    returns "True" if index finger is down 
"""
def checkIndexDown(lms):

    """ if no hand landmarks, return False. """
    if(len(lms) < 1 ):
        return False

    index_up = True

    """ index check landmarks index: 6, 7, 8 """
    if (lms[7][1] > lms[8][1]) or (lms[6][1] > lms[7][1]):
        return False

    for lm in lms[9:]:
        if (lm[1] > lms[8][1]):
            index_up = False
            break

    return index_up



""" This function checks if index and little fingers are up.
    returns "True" if index and little fingers are up 
"""
def checkIndexLittleUp(lms):

    """ if no hand landmarks, return False. """
    if(len(lms) < 1 ):
        return False

    index_little_up = True

    if (not checkIndexUp(lms)):
        return False

    """ little finger check landmarks index: 18, 19, 20 """
    if (lms[18][1] < lms[19][1]) or (lms[19][1] < lms[20][1]):
        return False

    for lm in lms[9:16]:
        if (lm[1] < lms[20][1]):
            index_little_up = False
            break

    return index_little_up

