
import cv2
import numpy as np
import time

def trackX(val):
    global xPosition
    xPosition = val
    print('X-position: ', xPosition)

def trackY(val):
    global yPosition
    yPosition = val
    print('Y-position: ', yPosition)

def trackW(val):
    global boxWidth
    boxWidth = val
    print('Box Width: ', boxWidth)

def trackH(val):
    global boxHeight
    boxHeight = val
    print('Box Height: ', boxHeight)

imgWidth = 1280
imgHeight = 720

textPosition = (20, 50)
font = cv2.FONT_HERSHEY_SIMPLEX
textSize = 1
textWeight = 2
textColor = (255, 0,  255)

boxColor = (0, 0, 255)

capture = cv2.VideoCapture(0)
capture.set(3, imgWidth)
capture.set(4, imgHeight)

cv2.namedWindow('My Trackbars')
cv2.createTrackbar('Xpos', 'My Trackbars', 10, imgWidth-1, trackX)
# x-position
# window name where track bar locates
# 10: initial(default) value
# imgWidth-1: max-value
# trackX: function name to control track bar
cv2.createTrackbar('Ypos', 'My Trackbars', 10, imgHeight-1, trackY)
cv2.createTrackbar('Box Width', 'My Trackbars', 10, imgWidth-1, trackW)
cv2.createTrackbar('Box Height', 'My Trackbars', 10, imgHeight-1, trackH)


start = time.time()
while True:
    ret, image = capture.read()
    image = cv2.flip(image, 1)
    # print(image[imgHeight//2, imgWidth//2])

    frameHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # print(frameHSV[imgHeight//2, imgWidth//2])

    end = time.time()
    fps = 1 / (end - start)
    cv2.putText(image, str(int(fps)) + ' FPS', textPosition, font, textSize, textColor, textWeight)
    cv2.rectangle(image, (xPosition, yPosition), (xPosition + boxWidth, yPosition + boxHeight), boxColor, 3)

    ROI = image[yPosition:yPosition+boxHeight, xPosition:xPosition+boxWidth]

    cv2.imshow('IMAGE', image)
    cv2.imshow('ROI', ROI)
    start = end

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()