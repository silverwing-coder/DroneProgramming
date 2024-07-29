# Tello drone keyboard control and image display
# Edited by Sangmork Park, May-2024

from djitellopy import Tello
import cv2
from time import sleep

import HelperKeyControl as kc

if __name__ == '__main__':

    drone = Tello()
    drone.connect()
    print(drone.get_battery())

    drone.streamon()
    # drone.takeoff()

    while True:

        frame = drone.get_frame_read().frame

        cv2.resize(frame, (300, 200))
        cv2.imshow('DRONE', frame)

        key = cv2.waitKey(5);
        print(key)
        vals = kc.getControlValue(key)
        print(vals[0], "-", vals[1], "-", vals[2], "-", vals[3])

        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        sleep(0.05)

        """ if 'q' pressed, break while loop """
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        if key == ord('q'):
            break

    drone.land()
    drone.streamoff()
    cv2.destroyAllWindows()
    exit()
