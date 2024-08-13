import socket
import cv2
import struct

import numpy as np

SERVER_IP = '10.42.0.1'
STREAM_PORT = 9999

# max UPD datagram size = 2**16
MAX_DGRAM = 2**16
# UPD header size = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64

class StreamClient:

    def __init__(self, soket, address = '127.0.0.1', port=9999):
        self.soket = soket
        self.address = address      # server address
        self.port = port            # server-port

    def dump_buffer(self):
        # emptying buffer
        while True:
            package, address = self.soket.recvfrom(MAX_DGRAM)
            print(package[0])
            if struct.unpack('b', package[0:1])[0] == 1:
                break

    def receive_video_stream(self):
        pass


def main():

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client = StreamClient(client_socket, SERVER_IP, STREAM_PORT)
        client_socket.sendto(b'Hello, Server!', (client.address, client.port))

        img_data = b''
        client.dump_buffer()

        while True:

            segment, address = client.soket.recvfrom(MAX_DGRAM)
            if struct.unpack("B", segment[0:1])[0] > 1:
                img_data += segment[1:]
            else:
                img_data += segment[1:]

                frame = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 1)
                # print(len(img_data))
                cv2.imshow('CLIENT WINDOW', frame)

                img_data = b''
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

    cv2.destroyAllWindows()
    client_socket.close()

if __name__ == '__main__':
    main()