import cv2, math, time
from ultralytics import YOLO

MODEL = YOLO("yolov8n-pose.pt")
def get_pose_results(frame):
    return  MODEL(frame, verbose=False, device='cpu', conf=0.7)

def get_annotated_frame_from_results(results) -> list:
    annotated_frame = results[0].plot()
    cv2.circle(annotated_frame, (320, 240), int(0.07 * math.dist((0, 0), (640, 480))), (0, 0, 255), 2)
    return annotated_frame

def get_control_command_from_results(results) -> list:
    # point of interest (node location on face): (poi_x, poi_y)

    poi_x, poi_y = results[0].keypoints.xyn[0][0][0], results[0].keypoints.xyn[0][0][1]
    # print(poi_x, ':', poi_y)
    image_center = (0.5, 0.5)

    # calculate distance between poi and image center (0.5, 0.5)
    distance = math.dist((poi_x, poi_y), image_center)
    print(round(distance, 2))

    hz_control = ''
    vt_control = ''

    if distance > 0.1: # (math.sqrt(2)*0.1 = 1.414 * 0.1)
        hz_control = 'LEFT' if poi_x > 0.5  else 'RIGHT'
        vt_control ='DOWN' if poi_y > 0.5  else 'UP'

    return (hz_control, vt_control)


def main():

    cap = cv2.VideoCapture(0)
    start = time.time()
    while (cap.isOpened()):
        success, frame = cap.read()

        if success:
            frame = cv2.flip(frame, 1)
            results = get_pose_results(frame)
            # results = model(frame, verbose=False, device='cpu', conf=0.7)

            annotated_frame = get_annotated_frame_from_results(results)
            # annotated_frame = results[0].plot()

            end = time.time()
            fps = round(1 / (end - start))
            cv2.putText(annotated_frame, 'FPS: ' + str(fps), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            cv2.imshow('YOLO', annotated_frame)

            print(get_control_command_from_results(results))

            time.sleep(0.01)

            start = end

            if (cv2.waitKey(1) == ord('q')):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()