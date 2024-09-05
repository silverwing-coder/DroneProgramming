import socket

bufferSz = 1024
msgFromServer = "Hello clients. Happy to be your server."
bytesToSend = msgFromServer.encode('utf-8')

serverIP = '192.168.39.125'
serverPort = 2222
RPISocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPISocket.bind((serverIP, serverPort))

print('Server is Up and Waiting .....')

cnt = 0
while True:
    message, address = RPISocket.recvfrom(bufferSz)
    message = message.decode('utf-8')
    print(message)
    print('Client address: ', address[0])

    if message == 'INC':
        cnt = cnt + 1

    if message == 'DEC':
        cnt = cnt - 1

    returnMsg = str(cnt)
    returnMsg = returnMsg.encode('utf-8')
    RPISocket.sendto(returnMsg, address)

    if cnt >= 5:
        break
