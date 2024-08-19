'''
This code controls Tello drone with OpenCV keyboard and displays image on OpenCV.
    - Updated by Sangmork Park, Jan-2023
'''

from djitellopy import Tello
import pygame
import cv2
from time import sleep


# Initialize pygame object. Must be in active mode to get keyboard input.
def initPygame():
    pygame.init()
    window = pygame.display.set_mode((300, 200))


# Check keyboard input and returns True if the pressed_key matches with keyName
'''
'LEFT'    : move left     'RIGHT'   : move right
 'UP'      : move back     'DOWN'    : move forward
 'W'       : move up       'S'       : move down
 'A'       : yaw left      'D'       : yaw right
'''

def getKey(keyName):
    for event in pygame.event.get():
        pass
    keyPressed = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))

    pygame.display.update()
    return keyPressed[myKey]


def getControlValue():

    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if getKey("LEFT"):
        lr = -speed
    elif getKey("RIGHT"):
        lr = speed

    if getKey("UP"):
        fb = speed
    elif getKey("DOWN"):
        fb = -speed

    if getKey("w"):
        ud = speed
    elif getKey("s"):
        ud = -speed

    if getKey("a"):
        yv = speed
    elif getKey("d"):
        yv = -speed

    return [lr, fb, ud, yv]


if __name__ == '__main__':

    initPygame()

    drone = Tello()
    drone.connect()
    print(drone.get_battery())

    drone.streamon()
    drone.takeoff()

    while True:

        frame = drone.get_frame_read().frame
        cv2.resize(frame, (300, 200))
        cv2.imshow('DRONE', frame)

        vals = getControlValue()
        print(vals[0], "-", vals[1], "-", vals[2], "-", vals[3])

        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        sleep(0.05)

        # if 'q' pressed, exit while loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    drone.land()
    drone.streamoff()
    cv2.destroyAllWindows()
    # exit()
