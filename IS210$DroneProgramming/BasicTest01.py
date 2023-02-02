# Tello drone basic movement test
# Edited by Sangmork Park, Jan-2023

""" 
This code tests Tello drone connection to Python code and basic movement.
Edited by Sangmork Park, Jan-2023
"""
from djitellopy import Tello
from time import sleep

# Create a arone object
drone = Tello()
drone.connect()
print(drone.get_battery())

drone.takeoff()
drone.move_up(30)
sleep(3)

drone.flip_forward()
sleep(3)
drone.flip_back()
sleep(3)

print(drone.get_barometer())
print(drone.get_flight_time())
drone.land()
