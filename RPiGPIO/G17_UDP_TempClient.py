import socket

bufferSz = 1024
serverAddress = ('192.168.39.125', 2222)

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    cmd = input('What do you want: GO or EXIT ')
    if cmd == 'EXIT':
        break

    cmd = cmd.encode('utf-8')
    UDPClient.sendto(cmd, serverAddress)

    data, address = UDPClient.recvfrom(bufferSz)
    data = data.decode('utf-8')

    print('Data from serfer: ', data)
    print('Server IP: ', address[0])
    print('Server Port: ', address[1])