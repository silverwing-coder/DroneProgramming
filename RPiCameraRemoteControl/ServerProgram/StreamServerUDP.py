'''
Edited by Sangmork Park, July-2024 
---------------------------------------------------------------------------
This Python program build a video streaming server captured by web camera.

---------------------------------------------------------------------------
'''

# This is server code to send video frames over UDP
import cv2, socket, imutils
import base64

from picamera2 import Picamera2  # type: ignore

BUFF_SIZE = 65536
SERVER_IP_ADDRESS = '10.42.0.1'
VIDEO_PORT_NUMBER = 9999

''' RPi Camera Set-up'''
IMG_WIDTH = 640
IMG_HEIGHT = 480

camera = Picamera2()
camera.preview_configuration.main.size = (IMG_WIDTH, IMG_HEIGHT)
camera.preview_configuration.main.format = "RGB888"     # 8 bit RGB format
camera.preview_configuration.align()                    # keep format size sililar to standard
camera.configure('preview')
camera.start()

video_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
video_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
# host_name = socket.gethostname()
# host_ip = '192.168.1.102'#  socket.gethostbyname(host_name)
# print(host_ip)

video_server_socket.bind((SERVER_IP_ADDRESS, VIDEO_PORT_NUMBER))
print(f'Listening at {SERVER_IP_ADDRESS}:{VIDEO_PORT_NUMBER} .....')

client_message, client_address = video_server_socket.recvfrom(BUFF_SIZE)
print('Connection from: ', client_address)

WIDTH = 400
while True:

	frame = camera.capture_array()
	frame = imutils.resize(frame, width=WIDTH)
	
	if_encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
	package = base64.b64encode(buffer)
	video_server_socket.sendto(package, client_address)
	# print('data sent ....')

