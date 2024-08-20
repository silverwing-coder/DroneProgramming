'''
Edited by Sangmork Park, June-2024
    - Get a thermal imsge from MLS90640 thermal camera via I2C
    - Process the image and display on matplotlib  

'''

import time
import board        # type: ignore
import busio        # type: ignore
import numpy as np
import adafruit_mlx90640            # type: ignore
import matplotlib.pyplot as plt     # type: ignore

# Setup I2C connection
# i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

plt.ion()
fig, ax = plt.subplots(figsize=(12, 7))
thermal = ax.imshow(np.zeros((24, 32)), vmin=0, vmax=60)
cbar = fig.colorbar(thermal)
cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)

# Initialize the array for all 768 temperature readings
frame = np.zeros((24*32))
t_array = []
max_retries = 5

while True:
    t1 = time.monotonic()
    retry_count = 0
    while retry_count < max_retries:
        try:
            mlx.getFrame(frame)
            # average_temf_c = np.mean(frame)
            # average_temf_f = (average_temf_c * 9 / 5) + 32.0
            # print(f'fAverage MLX90640 Temperature: {average_temf_c:.1f}C ({average_temf_f:.1f}F)')
            # time.sleep(.5)
            
            data_array = np.reshape(frame, (24, 32))
            thermal.set_data(np.fliplr(data_array))
            thermal.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.001)
            t_array.append(time.monotonic() - t1)
            print('Sample Rate: {0:2.1f} fps'.format(len(t_array)/np.sum(t_array)))
            break
        except ValueError as e:
            print(f'Failed to read temperature. retrying. Error: {str(e)}')
            time.sleep(.5)
        except KeyboardInterrupt:
            print("Exiting ...")
            exit(0)
        except Exception as e:
            print(f'An unexpected error occured: {str(e)}')