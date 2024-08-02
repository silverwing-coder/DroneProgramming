<h4>Last update: June-25-2024</h4>

<h3>Raspberry Pi Setup (RPi 4B)</h3>

<em><h4>1. Operating System: Raspberry Pi O.S.</h4></em>

A. Option-1: use Raspberry Imager

B. Option-2: download image file and flash the image with balenaEcher

   <ol>
    <li> Download Raspberry Pi O.S. image file </li>
    <li> Download balenaEcher (Portable version recommended)</li>
    <li> Excute Echer and flash it to micro-sd card</li>
   </ol>
   
<em><h4>2. Setup Environment</h4></em>
<ul>
<li> Shell command setup </li>

```
    $ raspi-config      // setup environments
```

<li> If RPi Lite Version is installed --> WiFi-setup: Open (create) "wpa_supplicant.conf" </li>

```
    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="vmicisdrone"
        psk="vmicisdronelab"
    }
```

<li>Install Visual Studio Code </li>

```
   $ sudo apt update
   $ sudo apt install code
```

<li>Setup as an RPi Access Point </li>
    - Wifi network icon --> Advanced Options-->Create Wireless Hotspot --> Set SSID name, Security, Password as necessary<br/>
    Refer to <a href="https://www.tomshardware.com/how-to/raspberry-pi-access-point">Turn RPi into a WiFi AP</a>

<li>//Under Construction// </li>

</ul>
