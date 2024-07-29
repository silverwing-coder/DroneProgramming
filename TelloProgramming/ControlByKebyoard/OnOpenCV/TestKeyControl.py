
# from djitellopy import Tello
import cv2
from time import sleep

import HelperKeyControl as kc

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        key = cv2.waitKey(10);
        vals = kc.getControlValue(key)
        print(vals[0], "-", vals[1], "-", vals[2], "-", vals[3])

        """ if 'q' pressed, break while loop """
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        if key == ord('q'):
            break

        cv2.imshow('FRAME', image)

    cv2.destroyAllWindows()
    exit()
