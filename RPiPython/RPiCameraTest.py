import cv2

# Open-CV will not capture the image directly in bullseye/bookworm OS version.
# You must use picamera2 library module (default library in Raspberry O.S.)
from picamera2 import Picamera2

# import mediapipe as mp

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)  # keep 30 frames/sec
piCam.preview_configuration.main.format = "RGB888"  # 8 bit RGB format
# make format size similar to standard one
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

while True:
    frame = piCam.capture_array()

    cv2.imshow('PiCAM', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()


# capture = cv2.VideoCapture(0)

# if not capture.isOpened():
#     print("Camera is not opened")
# else:

#     while True:

#         ret, image = capture.read()
#         cv2.imshow('FRAME', image)


#         if cv2.waitKey(1) == ord('q'):
#             break

#     capture.release()
#     cv2.destroyAllWindows()
