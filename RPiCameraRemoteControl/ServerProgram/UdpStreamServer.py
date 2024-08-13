'''
Edited by Sangmork Park, July-2024 
---------------------------------------------------------------------------
This Python program build a video streaming server captured by web camera.

---------------------------------------------------------------------------
'''

import socket
from picamera2 import Picamera2 # type: ignore
import cv2
import math

import struct

SERVER_IP = '10.42.0.1'
STREAM_PORT = 9999

# max UPD datagram size = 2**16 
MAX_DGRAM = 2**16
# UPD header size = 2**16 
MAX_IMAGE_DGRAM = MAX_DGRAM - 64

class StreamServer:

    def __init__(self, soket, address='127.0.0.1', port=9999):
        self.soket = soket
        self.address = address
        self.port = port

    def activate_stream_service(self, client_addr, camera):
        while True:
            frame = camera.capture_array()
            _, encoded_image = cv2.imencode('.jpg', frame)
            img_dgram = encoded_image.tobytes()
            img_dgram_size = len(img_dgram)
            pack_count = math.ceil(img_dgram_size/MAX_IMAGE_DGRAM)

            img_start = 0
            while pack_count:
                img_end = min(img_dgram_size, img_start + MAX_IMAGE_DGRAM)
                self.soket.sendto(struct.pack("B", pack_count) + img_dgram[img_start:img_end], client_addr)
                # print(f'packet sent...: {img_dgram_size}')
                
                img_start = img_end
                # img_dgram_size -= MAX_IMAGE_DGRAM
                pack_count -= 1

def main():
    
    camera = Picamera2()
    camera.preview_configuration.main.size = (640, 480)
    camera.preview_configuration.main.format = "RGB888"     # 8 bit RGB format
    camera.preview_configuration.align()                    # keep format size sililar to standard
    camera.configure('preview')
    camera.start()

    permitted_clients = ['10.42.0.200']

    # with statement automatically close the socket at the end of the block 
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server = StreamServer(server_socket, SERVER_IP, STREAM_PORT)
        server.soket.bind((server.address, server.port))
        print('UDP server is up and waiting ..... ')
                
        while True:
            received_data, client_id = server.soket.recvfrom(MAX_DGRAM)
            
            # security purpose:  check client's ip-address
            if client_id[0] in permitted_clients:
                server.activate_stream_service(client_id, camera)

                # print(received_data)
                # server.soket.sendto(received_data, client_id)
                # print(f' sent to {client_id[0]}')

if __name__ == '__main__':
    main()


