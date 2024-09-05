<h4>Created: June-25-2024</h4>
<h4>Last update: June-25-2024</h4>
<h3>Raspberry Pi Setup</h3>

<em><h4>Operating System: Raspberry Pi O.S.</h4></em>

A. Option-1: use Raspberry Imager

B. Option-2: download image file and flash the image with balenaEcher
   <ol>
    <li> Download Raspberry Pi O.S. image file </li>
    <li> Download balenaEcher (Portable version recommended)</li>
    <li> Excute Echer and flash it to micro-sd card</li>
   </ol>
   
<em><h4>Setup Environment</h4></em>
<ul>
<li> WiFi-setup: Open (create) "wpa_supplicant.conf" </li>

 ```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

 network={
        ssid="vmicisdrone"
        psk="vmicisdronelab"
}
 ``` 
    
<li>Boot  RPi and enable ssh server</li>

 ```
    $ raspi-config
         --> Interface Options
         --> Enable SSH 
 ```

<li>Install Visual Studio Code </li>

 ```
    $ sudo apt update
    $ sudo apt install code
 ```
<ul>