<h4>Last update: June-2024</h4>

<h2>Aerial Robotics: Drone Development - I</h2>

<h3>I. PixHawk Setup</h3>
<ol>
    <li> Download and install Ardupilot mission planner:<br/> 
    <a href="https://ardupilot.org/planner/docs/mission-planner-installation.html"> Ardupilot Mission Planner</a>
    </li>
    <li> Setup PixHawk on mission planner program
    </li>
</ol>


<h3>II. RPi-PixHawk Connection</h3>

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


<h3>III. Drone Programming</h3>

<h4>Drone</h4>

1. Drone Hardware

2. Flight Controller Hardware: PixHawk, RPi, ...

3. Flight Controller Software: Ardupilot, APM, PX4, ...

<h4>Communication Layer (Middleware) </h4>

1. Telemetry Module

2. MAVLINK

<h4>Ground Control</h4>

1. GCS Hardtware: Laptop, ....

2. GCS Software: QGroundControl, APM Planner, Mission Planner, "YOUR" Application, ....

3. Software Development API: DROKEKIT, ....


<h4>Ardupilot and SITL Setup</h4>

- Dowunload from GitHub Ardupilot and Setup environment 

    ``` sh
    # check the latest ardupilot firmware version ....
    $ git clone -b Copter-4.5.5 https://github.com/ardupilot/ardupilot
    $ cd ardupilotcd 
    $ git submodule update --init --recursive

    $ Tools/environment_install/install-prereqs-ubuntu.sh -y

    $ cd ardupilot
    $ ./waf list_boards

    # launch SITL simulator
    $ cd ArduCopter
    $ Tools/autotest/sim_vehicle.py --console --map -w

    # if pymavelink import problem meet
    $ git submodule update --init --recursive
    
    # if empy error meet
    $ sudo python -m pip install empy==3.3.4
    
    # if unable to find mavproxy.py error meet
    $ sudo pip install -U mavproxy
    ```
- What sim_vehicle.py do are
    
    1. Detect what vehicle to build for (Copter, Plane, Rover, ....)
    2. Compiles the necessary source code and produce an executable
    3. Launches the simulated drone by running the SITL executable
    4. Launches MAVProxy to communicate with the drone on SITL.

<h4>Dron Kit Install</h4>

```
$sudo -H pip install dronekit==2.9.2
$sudo -H pip install dronekit-sitl==3.3.0

```

<h4>Dron Kit Script Error Correction</h4>

1. ERROR: class Parameter(collections.MutableMapping, HasObservers) ... <br/>
-> go to "site-packages/dronekit/__inin__.py" line 2689 and revise "class Parameters(collections.MutableMapping, ...)" to "class Parameters(collections.abc.MutableMapping, ...)"

 


