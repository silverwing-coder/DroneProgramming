'''
Edited by Sangmork Park, June-2024
    - Get a thermal imsge from MLS90640 thermal camera via I2C
    - Process the image and display on matplotlib  

'''

import time
import board        # type: ignore
import busio        # type: ignore
import numpy as np
import adafruit_mlx90640        # type: ignore
import matplotlib.pyplot as plt # type: ignore

def initialize_sensor():
    i2c = busio.I2C(board.SCL, board.SDA)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ
    return mlx

def setup_plot():
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 7))
    thermal = ax.imshow(np.zeros((24, 32)), vmin=0, vmax=60, cmap='inferno', interpolation='bilinear')
    cbar = fig.colorbar(thermal)
    cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)
    plt.title('Thermal Image')
    return fig, ax, thermal

def update_display(fig, ax, thermal, data_array):
    thermal.set_data(np.fliplr(data_array))
    thermal.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))
    ax.draw_artist(ax.patch)
    ax.draw_artist(thermal)
    fig.canvas.update()
    fig.canvas.flush_events()

def main():
    mlx = initialize_sensor()
    fig, ax, thermal = setup_plot()

    frame= np.zeros((24*32))
    t_array = []
    max_retries = 5

    while True:
        t1 = time.monotonic()
        retry_count = 0
        while retry_count < max_retries:
            try:
                mlx.getFrame(frame)                
                data_array = np.reshape(frame, (24, 32))
                update_display(fig, ax, thermal, data_array)
                plt.pause(0.001)
                t_array.append(time.monotonic() - t1)
                print('Sample Rate: {0:2.1f} fps'.format(len(t_array)/np.sum(t_array)))
                break
            except ValueError as e:
                # print(f'Failed to read temperature. retrying. Error: {str(e)}')
                # time.sleep(.5)
                retry_count += 1
            except RuntimeError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(f'Failed after {max_retries} tries with error: {str(e)}')
                    break
            except KeyboardInterrupt:
                exit(0)

if __name__ == '__main__':
    main()