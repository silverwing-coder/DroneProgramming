'''
Edited by Sangmork Park, July-2024
-   This Pythond code displays web-camera image and get keyboard inputs which
    is used to control robots movement. 
-   Image display and pressed keyboard verification are implemented on opencv(cv2) library
    
@input: keyboard
@output: pressed key character

'''

import cv2
import time

capture = cv2.VideoCapture(0)

# variables for calculating frame-rate(fps): start, end
start = time.time()
while True:
    _, image = capture.read()

    image = cv2.flip(image, 1)
    end = time.time()
    fps = int(1 / (end - start))
    cv2.putText(image, str(fps), (30, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    cv2.imshow('OPENCV', image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("o"):
        print('UP')
    if key == ord("l"):
        print('DOWN')
    if key == ord("i"):
        print('LEFT')
    if key == ord("p"):
        print('RIGHT')
        
    if key == ord('q'):
        break
    start = end

cv2.destroyAllWindows()
capture.release()
