import time
import tty
import termios
import select
import os
import sys

from bella_hat.music import Music
from bella_hat.bella import Bella
from bella_hat.utils import run_command

# start the web camera  
#----------------------------------------------------------------
webcam_address = ""
webcam_done = False
try:
    from vilib import Vilib, utils

    Vilib.camera_start(vflip=True, hflip=False)
    Vilib.show_fps()
    Vilib.display(local=False, web=True)

    wlan0, eth0 = utils.getIP()
    if wlan0 != None:
        webcam_address += f"http://{wlan0}:9000/mjpg\n"
    if eth0 != None:
        webcam_address += f"http://{eth0}:9000/mjpg\n"

    webcam_done = True
except:
    webcam_address = ""
    webcam_done = False

# init bella 
#----------------------------------------------------------------
bella = Bella()
bella.motors.reverse([True, False])


# init music and sound effect files
#----------------------------------------------------------------
music = Music()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def horn(): 
    _status, _result = run_command('sudo killall pulseaudio')
    music.sound_play_threading(f'./car-double-horn.wav')

# global vars and print function
#----------------------------------------------------------------
forward_str = f'\033[1;30m{"↑"}\033[0m'
backward_str = f'\033[1;30m{"↓"}\033[0m'
left_str = f'\033[1;30m{"←"}\033[0m'
right_str = f'\033[1;30m{"→"}\033[0m'
power = 0
dir = "stop" 
eyes_state =  False

def update_print():
    global eyes_state

    batVolt = bella.get_battery_voltage()
    batPerc = bella.get_battery_percentage()
    batstrlen = int(batPerc / 10)
    bat_str = bat_str = "|"*batstrlen+" "*(10-batstrlen)
    distance = bella.get_ultrasonic_distance()
    temp = bella.get_temperature()
    hum = bella.get_humidity()
    grayscale = bella.get_grayscales()
    btn_state = bella.read_btn()
    acc = bella.get_acc()
    gyro = bella.get_gyro()
    power_l, power_r = bella.motors.speed()

    forward_str = f'\033[1;30m{"↑"}\033[0m'
    backward_str = f'\033[1;30m{"↓"}\033[0m'
    left_str = f'\033[1;30m{"←"}\033[0m'
    right_str = f'\033[1;30m{"→"}\033[0m'
    if dir == "forward":
        forward_str = f'\033[0;33m{"↑"}\033[0m'
    elif dir == "backward":
        backward_str = f'\033[1;33m{"↓"}\033[0m'
    elif dir == "left":
        left_str = f'\033[1;33m{"←"}\033[0m'
    elif dir == "right":
        right_str = f'\033[1;33m{"→"}\033[0m'

    info = f'''
webcam_address: {webcam_address}

    {forward_str}                Left   Right   Total
 {left_str}     {right_str}     power:  {power_l:03d}    {power_r:03d}      {power:03d}
    {backward_str}

Battery:      |{bat_str}|  {batPerc:.1f}  {batVolt:.2f} V
Ultrasonic:   {distance} cm
DHT11:        temperature: {temp}'C   humidity: {hum}%
LSM6DSOX:     acc: X:{acc[0]:.2f},    Y: {acc[1]:.2f},    Z: {acc[2]:.2f} m/s^2
              gyro X:{gyro[0]:.2f},    Y: {gyro[1]:.2f},    Z: {gyro[2]:.2f} radians/s
Grayscale:    {grayscale}
Fan:          {"on" if bella.fan_state else "off"}
Btn:          {"pressed" if btn_state else "released"}
Eyes:         {eyes_state}
Is_Charging:  {"Yes" if bella.read_charge_status() else "No"}

Move: [W,A,S,D]    STOP: [X]   Honk: [Q]   Fan: [E]    Eyes: [R]

    '''
    print('\033[H\033[J')
    print(info)


# keyboard detection
#----------------------------------------------------------------
settings = termios.tcgetattr(sys.stdin)
def getKey():
    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select.select([sys.stdin], [], [], 0.1) 
    if rlist:
        key = sys.stdin.read(1) 
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) 

    return key


# main
#----------------------------------------------------------------
def main():
    global dir, power, eyes_state

    st = 0
    while True:
        if time.time() - st > 1:
            update_print()
            st = time.time()

        _key = getKey().lower()

        if _key != '':
            if _key in ('wasdx'):
                if _key == 'w':
                    dir = 'forward'
                    # if power <= 0:
                    #     power = 20
                    # else:
                    #     power += 10
                    # if power > 100:
                    #     power = 100
                    # bella.set_motors(power, power)
                    bella.motors.forward(100)
                elif _key == 's':
                    dir = 'backward'
                    # if power >= 0:
                    #     power = -20
                    # else:
                    #     power -= 10
                    # if power < -100:
                    #     power = -100
                    # bella.set_motors(power, power)
                    bella.motors.backward(100)
                elif _key == 'a':
                    dir = 'left'
                    # bella.set_motors(-power, power)
                    bella.motors.turn_left(100)
                elif _key == 'd':
                    dir = 'right'
                    # bella.set_motors(power, power)
                    bella.motors.turn_right(100)
                elif _key == 'x':
                    dir = 'stop'
                    power = 0
                    # bella.set_motors(power, -power)
                    bella.motors.stop()
                update_print()
                st = time.time()
            elif _key == 'q':
                horn()
            elif _key == 'e':
                if bella.fan_state:
                    bella.fan_off()
                else:
                    bella.fan_on()
                update_print()
                st = time.time()
            elif _key == 'r':
                if eyes_state:
                    eyes_state = False
                    bella.set_eyes_led(0, 0)
                else:
                    eyes_state = True
                    bella.set_eyes_led(100, 100)
                update_print()
                st = time.time()

        time.sleep(.02)

if __name__ == "__main__":
    try:
        main()
    finally:
        bella.motors.stop()
        bella.set_eyes_led(0, 0)
        if webcam_done:
            Vilib.camera_close()
