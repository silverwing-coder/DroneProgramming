import cv2
import time

# Open-CV will not capture the image directly in bullseye/bookworm OS version.
# You must use picamera2 library module (default library in Raspberry O.S.)
from picamera2 import Picamera2

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
# 8 bit RGB format
camera.preview_configuration.main.format = "RGB888"     
 # keep format size sililar to standard
camera.preview_configuration.align()                   
camera.configure('preview')
camera.start()

start = time.time()

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
    if key == ord('q'):
        break

cv2.destroyAllWindows()
exit(0)

