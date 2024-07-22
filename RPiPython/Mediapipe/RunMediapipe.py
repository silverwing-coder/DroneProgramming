import cv2
import time
# Open-CV will not capture the image directly in bullseye/bookworm OS version. 
# You must use picamera2 library module (default library in Raspberry O.S.)
from picamera2 import Picamera2

# import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# import ModuleObjectDetection as mod
import ModuleHands as mh

piCam = Picamera2()
piCam.preview_configuration.main.size = (640, 480) # keep 30 frames/sec
piCam.preview_configuration.main.format = "RGB888"  # 8 bit RGB format
piCam.preview_configuration.align()                 # make format size similar to standard one
piCam.configure("preview")
piCam.start()

start_time = 0

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                           num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

while True:

    frame = piCam.capture_array()
    
    # results = mod.get_object_detection_results(frame)
    # frame = mod.get_annotated_image_objects(frame, results)

    results = mh.get_hands_detection_results(frame, detector)
    frame = mh.get_annotated_image_hands(frame, results)

    end_time = time.time()
    fps =  1 / (end_time - start_time)
    start_time = end_time

    fps = str (int (fps))
    cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 255, 0), 3, cv2.LINE_AA) 
    
    cv2.imshow('PiCAM', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
    