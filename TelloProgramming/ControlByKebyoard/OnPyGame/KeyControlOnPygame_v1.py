# Tello drone keyboard control and image display
# updated by Sangmork Park, July-2024

from djitellopy import Tello    # type: ignore 
import pygame                   # type: ignore
import time

# Check keyboard input. It returns True if the pressed key matches with a control key (key_name)
'''
 'LEFT' - move left,    'RIGHT' - move right,   'UP'    - move back,    'DOWN'  - move forward
 'W'    - move up,      'S'     - move down,    'A'     - yaw left,     'D'     - yaw right
'''
def check_key_pressed(key_name):
    for event in pygame.event.get():
        pass
    pressed_key = pygame.key.get_pressed()
    key_id = getattr(pygame, 'K_{}'.format(key_name))
    pygame.display.update()
    return pressed_key[key_id]

def get_control_commands() -> list:
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if check_key_pressed("LEFT"):
        lr = -speed
    elif check_key_pressed("RIGHT"):
        lr = speed

    if check_key_pressed("UP"):
        fb = speed
    elif check_key_pressed("DOWN"):
        fb = -speed

    if check_key_pressed("w"):
        ud = speed
    elif check_key_pressed("s"):
        ud = -speed

    if check_key_pressed("a"):
        yv = speed
    elif check_key_pressed("d"):
        yv = -speed

    return [lr, fb, ud, yv]


def main():
    pygame.init()

    drone = Tello()
    drone.connect()
    print(drone.get_battery())

    drone.streamon()
    drone.takeoff()

    frame = drone.get_frame_read()
    window = pygame.display.set_mode(frame.shape[1::-1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        frame = drone.get_frame_read()
        frame_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
        window.blit(frame_surf, (0, 0))
        pygame.display.flip()
        pygame.display.set_caption('PY-GAME')

        commands = get_control_commands()
        print(commands[0], "-", commands[1], "-", commands[2], "-", commands[3])
        drone.send_rc_control(commands[0], commands[1], commands[2], commands[3])
        time.sleep(0.05)

        if check_key_pressed('q'):
            break

    drone.land()
    drone.streamoff()
    pygame.quit()

if __name__ == '__main__':
    main()

