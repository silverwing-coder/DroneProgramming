import cv2
import time
from picamera2 import Picamera2

imgWidth = 640
imgHeight = 480

textPosition = (20, 50)
font = cv2.FONT_HERSHEY_SIMPLEX
textSize = 1
textWeight = 2
textColor = (255, 0,  255)

### text configuration for fps
textPosition = (20, 50)
font = cv2.FONT_HERSHEY_SIMPLEX
textSize = 1
textWeight = 2
textColor = (255, 0, 255)

### rectangle property
# rectUpperLeft = (100, 100)
# rectLowerRight = (200, 200)
# rectColor = (255, 255, 0)
# rectWeight = 2
# rectWeight = -1         # fill the box

### clrcle property

circlePx = 40
circlePy = 40
circleVx = 1
circleVy = 1

circleCenter = (circlePx + circleVx, circlePy + circleVy)
circleRadius = 40
circleColor = (255, 0, 255)
# rectWeight = 2
circletWeight = 3

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
    # imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imgROI = image[0:imgWidth//2, 0:imgHeight//2]

    end = time.time()
    fps = 1 / (end - start)

    cv2.putText(image, str(int(fps)) + ' FPS', textPosition, font, textSize, textColor, textWeight)
    # cv2.rectangle(image, rectUpperLeft, rectLowerRight, rectColor, rectWeight)

    # circleCenter = (circlePx, circlePy)
    # cv2.circle(image, circleCenter, circleRadius, circleColor, circletWeight)
    # circlePx = circlePx + circleVx
    # circlePy = circlePy + circleVy
    #
    # if (circlePx + circleRadius > 640 or circlePx - circleRadius < 0 ):
    #     circleVx = circleVx * -1
    # if (circlePy + circleRadius > 480 or circlePy - circleRadius < 0 ):
    #     circleVy = circleVy * -1

    cv2.imshow('IMAGE', image)
    cv2.imshow('ROI', imgROI)
    start = end

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()