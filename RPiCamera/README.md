<h4>Last update: 15 June 2024</h4>
<h3>Camera Module Installation on Raspberry Pi 4 Model B</h3>

1. Connect camera module to Raspberry Pi:
 <ul>
 <li>Locate the Camera Module port.</li>
 <li>Gently pull up on the edges of the port's plastic clip.</li>
 <li>Insert the Camera Module ribbon cable; make sure the connectors at the bottom of the ribbon cable are facing the contacts in the port.</li>
 <li>Push the plastic clip back into place.</li>
 </ul>
2. Enalble camera module
    ```
    $ sudo rpi-update
    $ sudo reboot
    $ libcamera-hello -t 0

    $ libcamera-still -t 5000
    ```
    <ul>
    <li>Close video window: "ALT + F4"</li>
    </ul>
    <br/>
    %%% The latest Respberry Pi O.S. include camera driver by default --> "No camera seup required!"
