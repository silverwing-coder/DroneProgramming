<em><h4>Edited by Sangmork Park, July-2024</h4></em>
<h3>Build IR Communiction for Drones on 38 KHz IR Tx/Rx modules</h3>

- Schematic: GND -- Vcc(5v) -- OUT(GPIO) 

<h4>1. References</h4>

- Refer to 

    1-1. <a href="https://www.digikey.com/en/maker/tutorials/2021/how-to-send-and-receive-ir-signals-with-a-raspberry-pi"> DigiKey Blog Page</a>

    1-2. <a href="https://github.com/BirchJD/RPiIR_Programmable_TV_Remote_Control"> Python Code Example (GitHub)</a>

    1-3.  <a href="https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/"> Brian Schwind's BLog</a>
    
    1-4.  <a href="https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/"> Brian Schwind's GitHub</a>
    

<h4>2. Environment Setup </h4>
    
    2.1 LIRC Protocol
- 
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

    2.2 pigpio ('Python' and 'C' libraries)

    'Python' and 'C' codes are implemented for transmitting data through IR communication network which provides alternative communication channel for drones in adversary / constrained operational environment of RF communication network.

    2.2.1 Data Transmission  on C-codes

    ```
    $ sudo systemctl kill pigpiod

    $ sudo ./a.out
    ```

    2.2.2 Python codes: 

    'Python' cannot accomplish exclusive occupation of CPU clocks due to the operating system on Raspberry Pi. To make exclusive control of gpio pins, kernel priviledged application execution is required. 'pigpio' library supports exclusive control of cpu time which is essential to generate accurate signal. --> Raspberry Pi rquires more complicate control programming compare to micro-contrillers

    <ol>
    <li>Install libpigpio C-library: Python script does not support kernel-level, fine-tuned GPIO control. libpigpio library supports kernel-level execution of application for stable GPIO PIN control. </li>

    ``` sh
    // Install libpigpio
    $ git clone https://github.com/joan2937/pigpio.git
    $ cd pigpio
    $ make
    $ sudo make install
    ```
    <li>Stop pigpio daemon </li>

    ``` sh
    $ sudo systemctl kill pigpiod

    ```
    <li>Run program on root previlege</li>

    ``` sh
    $ sudo application-name
    ```
    <li>When compile C-codes, link all necessary object files.</li>

    ``` sh
    $ gcc test.c -lm -lpigpio -pthread -lrt
    ```
    </ol>