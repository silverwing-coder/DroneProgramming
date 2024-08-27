import cv2
# import mediapipe as mp
from time import time

mp_face_detection = mp.solutions.face_detection
mp_face_detector = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def mpDetectFaces(image, mp_face_detector):

    image_height, image_width, _ = image.shape
    output_image = image.copy()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_face_detector.process(imgRGB)

    if results.detections:
        for face_no, face in enumerate(results.detections):
            mp_drawing.draw_detection(image=output_image, detection=face,
                                      keypoint_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0),
                                                                                   thickness=-1,
                                                                                   circle_radius=image_width // 230),
                                      bbox_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0),
                                                                               thickness=image_width // 360))
            face_bbox = face.location_data.relative_bounding_box

            x1 = int(face_bbox.xmin * image_width)
            y1 = int(face_bbox.ymin * image_width)

            # cv2.putText(output_image, text=str(round(face.score[0], 2)), org=(x1, y1 - 25),
            #             fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=image_width // 1200, color=(255, 255, 0),
            #             thickness=image_width // 300)
            cv2.putText(output_image, text=str(round(face.score[0], 2)), org=(x1, y1 - 25),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.7, color=(255, 0, 255),
                        thickness=2)

            # keypoints = face.location_data.relative_keypoints
            # print(keypoints)
            # 0: left-eye, 1: right-eye, 2: nose, 3: mouse, 4: left-ear, 5: right-ear

            # keypoint_idx = 0
            # for keypoint in face.location_data.relative_keypoints:
            #     cv2.putText(output_image, text=str(keypoint_idx), org=(int(keypoint.x*image_width), int(keypoint.y*image_height)),
            #             fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0, 255, 255),
            #             thickness=2)
            #     keypoint_idx = keypoint_idx + 1
                # print(keypoint_idx, ": [", int(keypoint.x*image_width), int(keypoint.y*image_height), "] ")

    return output_image, results.detections

def main():
    start_time = 0
    capture = cv2.VideoCapture(0)

    while (capture.isOpened()):
        success, frame = capture.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        frame, _ = mpDetectFaces(frame, mp_face_detector)

        # cv2.putText(frame, (frame_width // 3, frame_height // 8), cv2.FONT_HERSHEY_PLAIN, 4, (255, 155, 0), 3)
        end_time = time()

        if (end_time - start_time) > 0:
            frames_per_second = 1.0 / (end_time - start_time)

            cv2.putText(frame, 'FPS: {}'.format(int(frames_per_second)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

        start_time = end_time
        cv2.imshow('MediaPipe Face Detection', frame)
        # print(frame.shape)

        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
