
# Check keyboard input and returns if the pressed_key is a control key
# Returns 'true' only if the pressed key matches with keyName
"""
 'j'    : move left     'l'   : move right
 'i'    : move back     'k'   : move forward
 'e'    : move up       'd'   : move down
 's'    : yaw left      'f'   : yaw right
"""

def getControlValue(key):

    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if key == ord('j'):
        lr = -speed
        print(lr)
    elif key == ord('l'):
        lr = speed
        print(lr)

    if key == ord('i'):
        fb = -speed
        print(fb)
    elif key == ord('k'):
        fb = speed
        print(fb)

    if key == ord('d'):
        ud = -speed
    elif key == ord('e'):
        ud = speed

    if key == ord('s'):
        yv = -speed
    elif key == ord('f'):
        yv = speed

    return [lr, fb, ud, yv]