import cv2
import numpy as np
import time
from picamera2 import Picamera2

imgWidth = 1280
imgHeight = 720

textPosition = (20, 50)
font = cv2.FONT_HERSHEY_SIMPLEX
textSize = 1
textWeight = 2
textColor = (255, 0,  255)

# capture = cv2.VideoCapture(0)
# capture.set(3, imgWidth)
# capture.set(4, imgHeight)

hueLow = 20
hueHigh = 30
satLow = 100
satHigh = 255
vaLow = 100
valHigh = 255

lowerBound = np.array([hueLow, satLow, vaLow])
upperBound = np.array([hueHigh, satHigh, valHigh])

piCam = Picamera2()
piCam.preview_configuration.main.size = (imgWidth, imgHeight) # keep 30 frames/sec
piCam.preview_configuration.main.format = "RGB888"  # 8 bit RGB format
piCam.preview_configuration.align()                 # make format size similar to standard one
piCam.configure("preview")
piCam.start()

start = time.time()
while True:
    image = piCam.capture_array()
    image = cv2.flip(image, 1)
    # print(image[imgHeight//2, imgWidth//2])

    frameHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # print(frameHSV[imgHeight//2, imgWidth//2])
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)  # within range --> white, else --> black
    myMaskSmall = cv2.resize(myMask, (imgWidth//2, imgHeight//2))
    objectOfInterest = cv2.bitwise_and(image, image, mask = myMask)
    objectOfInterestSmall = cv2.resize(objectOfInterest, (imgWidth//2, imgHeight//2))

    end = time.time()
    fps = 1 / (end - start)
    cv2.putText(image, str(int(fps)) + ' FPS', textPosition, font, textSize, textColor, textWeight)

    cv2.imshow('IMAGE', image)
    cv2.imshow('MASK-SMALL', myMaskSmall)
    cv2.imshow('OBJECT-OF_INTEREST', objectOfInterestSmall)
    start = end

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()