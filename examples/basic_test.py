import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from bella_hat.pin import Pin
from bella_hat.music import Music
from bella_hat.bella import Bella
import readchar
import threading
# from vilib import Vilib, utils
import os

# Vilib.camera_start(vflip=True, hflip=False)
# Vilib.show_fps()
# Vilib.display(local=False, web=True)
# Vilib.color_detect(color="red")

# wlan0, eth0 = utils.getIP()
# camera_address = ""
# if wlan0 != None:
#     camera_address += f"http://{wlan0}:9000/mjpg\n"
# if eth0 != None:
#     camera_address += f"http://{eth0}:9000/mjpg\n"

bella = Bella()
try:
    i2c = board.I2C()
    imu = LSM6DSOX(i2c)
except:
    print("LSM6DSOX Error")

fan = Pin(16, mode=Pin.OUT)
fan.off()
btn = Pin(25, mode=Pin.IN)


batVolt = 0.00
batPerc = 0.0
bat_str = "|"*0+" "*10
distance = 0
temp = 0.0
hum = 0
grayscale = [0, 0, 0]
acc = [0.00, 0.00, 0.00]
gyro = [0.00, 0.00, 0.00]
forward_str = f'\033[1;30m{"↑"}\033[0m'
backward_str = f'\033[1;30m{"↓"}\033[0m'
left_str = f'\033[1;30m{"←"}\033[0m'
right_str = f'\033[1;30m{"→"}\033[0m'
power_l = 0
power_r = 0
power_t = 0
power = 0
dir = "stop" 
fan_state = False

music = Music()
User = os.popen('echo ${SUDO_USER:-$LOGNAME}').readline().strip()
UserHome = os.popen('getent passwd %s | cut -d: -f 6' %User).readline().strip()

def horn(): 
    _status, _result = utils.run_command('sudo killall pulseaudio')
    music.sound_play_threading(f'{UserHome}/bella-hat/examples/car-double-horn.wav')

def update_print():
    global batVolt, batPerc, bat_str, acc, gyro, fan_state
    batVolt = bella.getBatteryVoltage()
    batPerc = bella.getBatteryPercentage()
    batstrlen = int(batPerc / 10)
    bat_str = bat_str = "|"*batstrlen+" "*(10-batstrlen)
    distance = bella.getUltrasonicDistance()
    # temp,hum = bella.dht11.read_data()
    temp = bella.getTemperature()
    hum = bella.getHumidity()
    grayscale = bella.getGrayscales()
    btn_state = btn.value()

    try:
        acc = imu.acceleration
        gyro = imu.gyro
    except:
        pass
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

# camera_address: {#camera_address}

    info = f'''

    {forward_str}                Left   Right   Total
 {left_str}     {right_str}     power:  {power_l:03d}    {power_r:03d}      {power:03d}
    {backward_str}

Battery:      |{bat_str}|  {batPerc:.1f}  {batVolt:.2f} V
Ultrasonic:   {distance} cm
DHT11:        temperature: {temp}'C   humidity: {hum}%
LSM^DSOX:     acc: X:{acc[0]:.2f},    Y: {acc[1]:.2f},    Z: {acc[2]:.2f} m/s^2
              gyro X:{gyro[0]:.2f},    Y: {gyro[1]:.2f},    Z: {gyro[2]:.2f} radians/s
Grayscale:    {grayscale}
Fan:          {"on" if fan_state else "off"}
Btn:          {btn_state}

STOP: [X]   Honk: [Q]   Fan: [E]    Rec: [R]    Play: [P]

    '''
    print('\033[H\033[J')
    print(info)


key = ''
key_thread_lock = threading.Lock()
def key_handler():
    global key
    while True:
        _key = readchar.readkey().lower()
        with key_thread_lock:
            key = _key
        time.sleep(.1)

key_thread = threading.Thread(target=key_handler)
key_thread.daemon = True

def main():
    global key, dir, power, fan_state

    key_thread.start()
    
    st = 0
    while True:
        if time.time() - st > 0.8:
            update_print()
            st = time.time()

        _key = ''
        with key_thread_lock:
            _key = key
            if _key != '':
                key = ''
        # print(_key)
        if _key != '':
            if _key in ('wasdx'):
                # print('wasdx')
                if _key == 'w':
                    dir = 'forward'
                    if power <= 0:
                        power = 20
                    else:
                        power += 10
                    if power > 100:
                        power = 100
                    bella.motors.speed([power, power])
                elif _key == 's':
                    dir = 'backward'
                    if power >= 0:
                        power = -20
                    else:
                        power -= 10
                    if power < -100:
                        power = -100
                    bella.motors.speed([power, power])
                elif _key == 'a':
                    dir = 'left'
                    bella.motors.speed([-power, power])
                elif _key == 'd':
                    dir = 'right'
                    bella.motors.speed([power, power])
                elif _key == 'x':
                    dir = 'stop'
                    power = 0
                    bella.motors.speed([power, -power])
                update_print()
                st = time.time()
            elif _key == 'q':
                horn()
            elif _key == 'e':
                if fan_state:
                    fan_state = False
                    fan.off()
                else:
                    fan.on()
                    fan_state = True

        time.sleep(.1)

if __name__ == "__main__":
    main()
