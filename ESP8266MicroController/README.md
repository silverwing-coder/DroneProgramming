<h4>Last update: Aug. 2024 by <em>Sangmork Park at VMI</em></h4>


<h3>I. ESP8266 initial Setup and connection to Laptop computer</h3>

1. Connect USB: Micro-USB to Laptop

2. Windows:

    - Verify connection: Device Manager -> Other Devices -> CP2102 USB to UART Bridge Controller
    - <a href="https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads">Download 'CP210x Windows Drivers' </a>and install driver
    - Verify driver installation: Device Manager -> Port(COM & LPT) -> Silicon Labs CP210x USB to UART Bridge (COM3)

3. <a href="https://www.arduino.cc/en/software">Download</a> and install Ardunio IDE 

    - Open Ardunio IDE
    
    - Go to google -> "arduino nodemcu esp8266 github" -> GitHub support page -> Installing with Boards Manager -> Follow instructions ....

4. Create and save a Sketch file (*.ino)

    - Tools -> Board -> esp8266 -> "NodeMCU 1.0 xxxx"
    - Port -> COM3 (Select installed port)
    - Compile and Upload the code with the arrow key on Left-Upper corner

<h3>III. Serial Communication between RPi 5 and ESP8266 via USB </h3>

1. Connect USB and check device 

``` sh
$ ls /dev/      # check device: USB0  
```

2. Select serial Tx-Rx device 

``` py
    # serial communication via USB port'
    com_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
```


<h3>III. Serial Communication between RPi 5 and ESP8266 via UART </h3>

- Refer to <a href="https://electrosome.com/uart-raspberry-pi-python/">electroSome Tutorial Page</a> 

1. Enable serial port (UART)

``` sh
$ sudo raspi-config
# --> Interface Options --> Serial Port .... 

$ ls /dev/      # check device: AMA0  
```

2. Pin-out
    - ESP8266:  Tx -> GPIO 1, Rx -> GPIO 3
    - RPi:      Tx -> GPIO 14, Rx -> GPIO 15

3. Select serial Tx-Rx device 

``` py
    #serial communication via UART pins
    com_port = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
```
