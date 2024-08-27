
import cv2
import socket
import struct
import numpy as np
import threading
# import multiprocessing
import time
# import mediapipe as mp
# import MpFaceDetectionModule as fdm
import ImageProcessingModule as ipm
import YoloPoseModule as ypm

from pynput.keyboard import Key, Listener # type: ignore

# SERVER_IP_ADDRESS = '127.0.0.1'
SERVER_IP_ADDRESS = '10.42.0.1'
STREAM_PORT = 9999
TCP_CONTROL_PORT = 8888
UDP_CONTROL_PORT = 9988

MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64

''' initialize mediapipe face detector '''
# mp_face_detection = mp.solutions.face_detection
# mp_face_detector = mp_face_detection.FaceDetection(min_detection_confidence=0.4)
# mp_drawing = mp.solutions.drawing_utils

''' streaming server connection'''
stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, STREAM_BUFFER_SIZE)
message = b'Hi Server'
stream_socket.sendto(message,(SERVER_IP_ADDRESS, STREAM_PORT))

''' tcp_control server connection '''
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_socket.connect((SERVER_IP_ADDRESS, TCP_CONTROL_PORT))
print(f'Connected to .... {SERVER_IP_ADDRESS}:{TCP_CONTROL_PORT}')

''' udp_control server connection '''
control_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b'Hi udp control.'
control_socket1.sendto(message,(SERVER_IP_ADDRESS, UDP_CONTROL_PORT))

def handle_key_control1(key):
    if key == Key.up:
        control_socket.send('UP'.encode('ascii'))
    if key == Key.down:
        control_socket.send('DOWN'.encode('ascii'))
    if key == Key.left:
        control_socket.send('RIGHT'.encode('ascii'))
    if key == Key.right:
        control_socket.send('LEFT'.encode('ascii'))
    if key == 'q':
        control_socket.send('EXIT'.encode('ascii'))
        return False
    time.sleep(0.05)

def dump_buffer(stream_socket):
    # emptying buffer
    while True:
        package, address = stream_socket.recvfrom(MAX_DGRAM)
        print(package[0])
        if struct.unpack('b', package[0:1])[0] == 1:
            break

def key_control():
    with Listener(on_press=handle_key_control1) as listener:
        listener.join()


def main() -> None:

    ''' multiprocessing-scheme must implement key-exchange mechanism
     -> thread preferred ..... '''
    # control_thread = multiprocessing.Process(target=key_control)
    control_thread = threading.Thread(target=key_control)
    control_thread.daemon = True
    control_thread.start()

    ''' stream client implementation '''
    img_data = b''
    dump_buffer(stream_socket)
    while True:
        segment, address = stream_socket.recvfrom(MAX_DGRAM)
        if struct.unpack("B", segment[0:1])[0] > 1:
            img_data += segment[1:]
        else:
            img_data += segment[1:]

            frame = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 1)
            # print(len(img_data))
            if(frame is not None):
                # processed_frame = ipm.process_image(frame)
                # image, faces = fdm.mpDetectFaces(frame, mp_face_detector)
                results = ypm.get_pose_results(frame)
                image = ypm.get_annotated_frame_from_results(results)
                cv2.imshow('CLIENT WINDOW', image)

                if(results[0]):
                    # print(ypm.get_control_command_from_results(results))
                    control_socket1.sendto(ypm.get_control_command_from_results(results)[0].encode('ascii'),(SERVER_IP_ADDRESS, UDP_CONTROL_PORT))
                    control_socket1.sendto(ypm.get_control_command_from_results(results)[1].encode('ascii'),(SERVER_IP_ADDRESS, UDP_CONTROL_PORT))

            img_data = b''
            if cv2.waitKey(1) & 0xff == ord('q'):
                # cv2.destroyAllWindows()
                break

        # control_socket1.sendto(b'test control.', (SERVER_IP_ADDRESS, UDP_CONTROL_PORT))

    cv2.destroyAllWindows()
    stream_socket.close()
    control_socket.close()

if __name__ == '__main__':
    main()