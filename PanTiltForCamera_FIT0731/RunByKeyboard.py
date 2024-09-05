import cv2
import time
from picamera2 import Picamera2

from PCA9685 import PCA9685
import RPi.GPIO as GPIO

## manage image size to keep 30 fps 
imgWidth = 640
imgHeight = 480

## text configuration to display fps
textPosition = (20, 50)
font = cv2.FONT_HERSHEY_SIMPLEX
textSize = 1
textWeight = 2
textColor = (25, 0, 255)
pan = 80
tilt  = 5

camera = Picamera2()
camera.preview_configuration.main.size = (imgWidth, imgHeight)
camera.preview_configuration.main.format = "RGB888"     # 8 bit RGB format
camera.preview_configuration.align()                    # keep format size sililar to standard
camera.configure('preview')
camera.start()

start = time.time()

pwm = PCA9685()
pwm.setPWMFreq(50)
pwm.setRotationAngle(0, tilt)
pwm.setRotationAngle(1, pan)

while True:
    image = camera.capture_array()
    image = cv2.flip(image, 1)          # mirror view
    # imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imgROI = image[0:imgWidth//2, 0:imgHeight//2]

    end = time.time()
    fps = 1 / (end - start)
    cv2.putText(image, str(int(fps))+'FPS', textPosition, font, textSize, textColor, textWeight)

    cv2.imshow('IMAGE', image)
    # cv2.imshow('ROI IMAGE', imgROI)
    start = end

    key = cv2.waitKey(1)

    '''
    UP -> o, DOWN --> l, LEFT --> i, RIGHT --> p
    '''
    if key & 0xFF == ord('i'):      # LEFT
        if (pan >= 10):
            pan = pan - 1
    if key & 0xFF == ord('p'):      # RIGHT
        if (pan <= 170):
            pan = pan + 1
    if key & 0xFF == ord('o'):      # UP
        if (tilt >= 5):
            tilt = tilt - 1
    if key & 0xFF == ord('l'):      # DOWN
        if (tilt <= 70):
            tilt = tilt + 1
    if key == ord('q'):
        break

    pwm.setRotationAngle(0, tilt)
    pwm.setRotationAngle(1, pan)
    # time.sleep(0.1)
    # if cv2.waitKey(1) == ord('q'):
    #     break

cv2.destroyAllWindows()
