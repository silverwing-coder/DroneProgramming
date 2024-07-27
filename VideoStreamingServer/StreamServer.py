'''
Edited by Sangmork Park, July-2024 
---------------------------------------------------------------------------
This Python program build a video streaming server captured by web camera.

---------------------------------------------------------------------------
'''

import cv2
import socket
import pickle
import struct

SERVER_IP_ADDRESS = '127.0.0.1'
SERVER_PORT_NUMBER = 9999
CLIENT_PORT_NUMBER = 4096

video_capture = cv2.VideoCapture(0)

# Create a server socket for streaming
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP_ADDRESS, SERVER_PORT_NUMBER))     

# Maximum queue size of client requests: 10
server_socket.listen(10)                    

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"[*] Accepted connection from {client_address}")

while True:
    # Read a frame from the camera
    ret, frame = video_capture.read()

    # Serialize the frame to bytes
    serialized_frame = pickle.dumps(frame)

    # Pack the data size and frame data
    message_size = struct.pack("L", len(serialized_frame))
    client_socket.sendall(message_size + serialized_frame)

    # Display the frame on the server-side (optional)
    cv2.imshow('Server Video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()