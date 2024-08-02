<h4>Last update: June-26-2024</h4>
<h3>PixHawk Setup</h3>
<ol>
    <li> Download and install Ardupilot mission planner:<br/> 
    <a href="https://ardupilot.org/planner/docs/mission-planner-installation.html"> Ardupilot Mission Planner</a>
    </li>
    <li> Setup PixHawk on mission planner program
    </li>
</ol>


<h3>RPi-PixHawk Connection</h3>

--> Refer to <a href="https://www.youtube.com/watch?v=nIuoCYauW3s&t=246s">How to Connect PixHawk to Raspberry Pi</a> 

1. Setup Raspberry Pi
    - Connect RPi GPIO pins to Telemetry2 on pixhawk 
    - 5 V vcc, GND, TXD(pin #14), RXD(pin #15) 

2. Enable Serial Port

    ```
    $ sudo raspi-config
        --> Serial Port
        --> login shell to be accessible over serial: "NO"
        --> serial port hardware to be enabled: "YES"
        
    ```
3. Install APIs / libraries

    ```
    $ sudo apt install python3-dev
    $ sudo apt install python3-opencv
    $ sudo apt install python3-wxgtk4.0
    $ sudo apt install python3-matplotlib
    $ sudo apt install python3-lxml
    $ sudo apt install libxml2-dev
    $ sudo apt install libxslt-dev

    $ sudo pip install PyYAML --break-system-package
    $ sudo pip install mavproxy --break-system-package 

    $ sudo mavproxy.py --master=/dev/ttyAMA0
    
    ```

3. Test connection

    ```
    $ sudo mavproxy.py --master=/dev/ttyAMA0
    
    ```

<h2>//Under Costruction//</h2>
