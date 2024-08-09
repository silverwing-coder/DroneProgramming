<h4>Last update: June-25-2024</h4>

<h3>Raspberry Pi - Python Programming</h3>

<em><h4>1. Operating System: Raspberry Pi O.S.</h4></em>

    A. Option-1: use Raspberry Imager

    B. Option-2: download image file and flash the image with balenaEcher

<ol>
    <li> Download Raspberry Pi O.S. image file </li>
    <li> Download balenaEcher (Portable version recommended)</li>
    <li> Excute Echer and flash it to micro-sd card</li>
</ol>
   
<em><h4>2. Network Environment</h4></em>
<ol>
<li> WiFi setup </li>

```
    - country=US
    - SSID: VMI-Sentinal or eduroam
    - Sign-in Info: PEAP, no-certificate required
    - VMI ID and PW 
```

<li>RPi Access Point setup</li>
    - Wifi network icon --> Advanced Options-->Create Wireless Hotspot --> Set SSID name, Security, Password as necessary<br/>
    Refer to <a href="https://www.tomshardware.com/how-to/raspberry-pi-access-point">Turn RPi into a WiFi AP</a> <br/>
    
</ol>

<em><h4>3. Programming</h4></em>
<ol>
<li> GPIO Pin and Input/Output devices </li>

``` sh
    $ raspi-config      --> setup environments
```
<li>Python Virtual Environment:  </li>

<em>It is recommended to import all system site packages to use system library with option of "--system-site-packages". (Rasberry Pi provides numerous default python packages in the O.S.  Use the libraries within the virtual environment)</em>

``` sh   
    $ python3 -m venv --system-site-packages venv

    # Activate python virtual environment
    $ source venv/bin/activate

    # Install packages within virtual environment
    $ pip install <package-name>
    $ pip list

    $ pip install opencv-python
    $ pip install mediapipe


    # If system wide package installation is required
    $ sudo apt install python3-opencv
    
    # De-activate python virtual environment    
    $ source venv/bin/activate

```

<li>Install Visual Studio Code </li>

``` sh
   $ sudo apt update
   $ sudo apt install code
```

</ol>