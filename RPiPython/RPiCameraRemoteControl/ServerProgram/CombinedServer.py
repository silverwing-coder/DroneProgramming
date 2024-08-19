'''
Edited by Sangmork Park, August-2024 
---------------------------------------------------------------------------
This Python program controls Raspberry Pi Camera on a pan-tilt(FIT0731)
which provides video streaming service.
---------------------------------------------------------------------------
'''

import cv2
import socket
import math
import struct
import multiprocessing
# import threading

from picamera2 import Picamera2
from PCA9685 import PCA9685

# SERVER_IP_ADDRESS = '127.0.0.1'
SERVER_IP = '10.42.0.1'
STREAM_PORT = 9999
CONTROL_PORT = 8888

MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64

''' Set Raspberry Pi Pan-Tilt '''
tilt_angle = 45
pan_angle = 120
controller = PCA9685()
controller.setPWMFreq(50)
controller.setRotationAngle(0, tilt_angle)
controller.setRotationAngle(1, pan_angle)

def move_pan_tilt(command) -> None:
    # print('CMD:', command)
    global pan_angle, tilt_angle
    if command == 'LEFT':                   # LEFT
        if (pan_angle >= 10):
            pan_angle = pan_angle - 0.5
    if command == 'RIGHT':                  # RIGHT
        if (pan_angle <= 175):
            pan_angle = pan_angle + 0.5
    if command == 'UP':                     # UP
        if (tilt_angle >= 15):
            tilt_angle = tilt_angle - 0.5
    if command == 'DOWN':                   # DOWN
        if (tilt_angle <= 110):
            tilt_angle = tilt_angle + 0.5            
    # time.sleep(0.05)
    controller.setRotationAngle(0, tilt_angle)
    controller.setRotationAngle(1, pan_angle)

def handle_control_client(pipe) -> None:

    ''' control server socket '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as control_socket:
    # control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.bind((SERVER_IP, CONTROL_PORT))
        control_socket.listen()
        print('control server listening .....') 

        control_client, control_client_address = control_socket.accept()
        # print(f'Control client from {control_client_address}')
        control_client.send(f'Connected to Server ....'.encode('ascii'))

        while True:
            command = control_client.recv(1024).decode('ascii')
            # print(command)
            
            move_pan_tilt(command)
            # pipe.send('ON')
            status = 'Pan: ' + str(pan_angle) + ', Tilt: ' + str(tilt_angle) 
            # print(status) 
            control_client.send(status.encode(('ascii')))

def handle_stream_client(pipe) -> None:
    
    ''' Set Raspberry-Pi Camera '''
    IMG_WIDTH = 640
    IMG_HEIGHT = 480

    camera = Picamera2()
    camera.preview_configuration.main.size = (IMG_WIDTH, IMG_HEIGHT)
    camera.preview_configuration.main.format = "RGB888"     # 8 bit RGB format
    camera.preview_configuration.align()                    # keep format size sililar to standard
    camera.configure('preview')
    camera.start()

    # permitted_clients = ['10.42.0.200']
    ''' streaming server socket '''    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as stream_socket:
        # stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # stream_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, MAX_DGRAME)
        stream_socket.bind((SERVER_IP, STREAM_PORT))
        print('Streaming server listening .....')
    
        while True:
            received_data, client_id = stream_socket.recvfrom(MAX_DGRAM)
            # if client_id[0] in permitted_clients:
            while True:
                frame = camera.capture_array()
                _, encoded_image = cv2.imencode('.jpg', frame)
                img_dgram = encoded_image.tobytes()
                img_dgram_size = len(img_dgram)
                pack_count = math.ceil(img_dgram_size/MAX_IMAGE_DGRAM)

                img_start = 0
                while pack_count:
                    img_end = min(img_dgram_size, img_start + MAX_IMAGE_DGRAM)
                    stream_socket.sendto(struct.pack("B", pack_count) + img_dgram[img_start:img_end], client_id)
                    # print(f'packet sent...: {img_dgram_size}')
                            
                    img_start = img_end
                    pack_count -= 1

    
def main() -> None:

    # stream_thread = threading.Thread(target=handle_stream_client)
    # stream_thread.daemon = True
    stram_pipe, control_pipe = multiprocessing.Pipe()
    stream_process = multiprocessing.Process(target=handle_stream_client, args=[stram_pipe, ])
    stream_process.start()
        
    # control_thread = threading.Thread(target=handle_control_client)
    # control_thread.daemon = True
    control_process = multiprocessing.Process(target=handle_control_client, args=[control_pipe, ])
    control_process.start()


if __name__ == '__main__':
    main()