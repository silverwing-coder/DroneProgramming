import socket
import time

bufferSize = 1024
msgFromServer = "Hello client! I am happy to be your server."

serverPort = 2222
serverIp = '192.168.39.125'

bytesToSend = msgFromServer.encode('utf-8')
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP protocol
RPIsocket.bind((serverIp, serverPort))

print('Server is up and listening .....')

message, address = RPIsocket.recvfrom(bufferSize)
message = message.decode('utf-8')
print(message)
print('Client Address', address[0])         # address[0] --> IP address
RPIsocket.sendto(bytesToSend, address)

