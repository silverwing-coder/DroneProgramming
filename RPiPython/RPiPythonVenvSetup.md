<h4>Last update: 15 June 2024</h4>
<h3>Python Virtual Environment Setup and Activate</h3>

1. Python Virtual Environment setup:
    <em>You must import all system site packages to use system library with option of "--system-site-packages" </em>
    ```
    $ python3 -m venv --system-site-packages venv    
    /* Rasberry Pi provides numerous default python packages in the O.S.  To use the libraries within the virtual environment created, "--system-site-packages" option required. */
    ```
2. Activate Python Virtual Environment 
    ```
    $ source venv/bin/activate
    ```

3. Install packages within Virtual Environment 
    ``` 
    $ pip install <package-name>  
    // install package in the venv only
    $ pip list

    $ pip install opencv-python
    $ pip install mediapipe 
    

    // if system wide package installation is required
    $ sudo apt install python3-opencv    
    ```

4. De-ativate Python Virtual Environment 
    ```
    $ deactivate
    ```
