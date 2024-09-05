<h4>Last Update: July-2024</h4>
<h3>IR Communiction by 38 KHz IR Tx and Rx modules</h3>

<h4>Environment Set Up</h4>

1. Receiver / Transmitter on Python
    - Refer to 

    1-1. <a href="https://www.digikey.com/en/maker/tutorials/2021/how-to-send-and-receive-ir-signals-with-a-raspberry-pi"> DigiKey Blog Page</a>

    1-2. <a href="https://github.com/BirchJD/RPiIR_Programmable_TV_Remote_Control"> Python Code Example (GitHub)</a>

    1-3.  <a href="https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/"> Brian Schwind BLog</a>
    
    - Schematic: GND -- Vcc(3.3v) -- OUT(GPIO) 
    ```
    $ sudo nano /boot/firmware/config.txt
    ----------------------------------------
    # for data Rx
    dtoverlay=gpio-ir, gpio_pin=21
    # for data Tx
    dtoverlay=gpio-ir-tx, tpio_pin=20
    ----------------------------------------
    $ sudo reboot

    $ sudo apt update
    
    # Install a helper program that handles the parsing of raw timings and map them userdefined keys.
    # System will listen for the predefined series of timing sand raise a system-wide event when they occur
    $ sudo apt install ir-keytable

    <!-- 
    $ sudo ir-keytable -c -p all -t     --> test with remote control
    ---------------------------------------
    Error: unable to attach bpf problem, 
    lirc device name was not found
    --------------------------------------- 
    -->

    # Install LIRC(Linux Infra Red Remote Control)
    $ sudo apt install lirc
    $ sudo nano /etc/lirc/lirc_options.conf
    ---------------------------------------
    driver = default
    device = /dev/lirc0
    ---------------------------------------
    $ sudo reboot

    $ sudo systemctl stop lircd.service
    $ mode2 -d /dev/lirc0           --> test with remote control

    ```

2. Transmitter on C
    - Refer to 

    2-1.  <a href="https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/"> Brian Schwind BLog</a>

    ```
    $ sudo systemctl kill pigpiod

    $ sudo ./a.out
    ```
