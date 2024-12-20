# Setup 
#
# Disable Serial Console and enable Serial Port
# sudo raspi-config
# Interfacing Options -> Serial -> No -> Yes
# 
# Reboot the Raspberry Pi
#
# Port: /dev/ttyS0
# Baudrate: 115200
#
# Run the following command in the terminal to start the serial listener:
# python3 serial_command.py
#
# 测试命令通过串口发送。每次发送需要需要带新行
#
# 数据开        开始发送传感器数据
# 数据关        停止发送传感器数据
# 老化          测试常开电机风扇，老化
# 电机          测试电机，小车前进，速度慢慢变快再变慢，到后退，速度变快再变慢，到停止，随后左转，右转，停止
# 风扇          测试风扇，风扇开2秒，风扇关2秒
# 录播          录音3秒后，播放录音
# 喇叭          播放音乐
# 灯            测试灯环，红绿蓝白灯环，随后停止
# 相机          拍摄照片并传回base64格式图片
# AP:XXXXXXX    设置AP名称为XXXXXXX

import serial
import threading
import time
import logging
import json
from logging.handlers import RotatingFileHandler

from bella_hat.bella import Bella
from rpi_ws281x import PixelStrip, Color

APP_NAME = 'bella-serial-test-daemon'
# ENCODING = 'gbk'
ENCODING = 'utf-8'
AP_NAME_PREFIX = 'bella-'
USER_NAME = 'xo'
TEST_MUSIC_FILE = f'/opt/{APP_NAME}/test_music.wav'
TEST_RECORD_FILE = f'/opt/{APP_NAME}/test_record.wav'
TEST_IMAGE_FILE = f'/opt/{APP_NAME}/test_image.jpg'
FACTORY_MODE_AUDIO = f'/opt/{APP_NAME}/factory-mode.wav'
APNAME_FILE = f'/opt/{APP_NAME}/apname.txt'
TEST_IMAGE_WIDTH = 320
TEST_IMAGE_HEIGHT = 240
TEST_IMAGE_ROTATION = 180
LOG_FILE = f'/var/log/{APP_NAME}.log'

TAG_LOG = "[LOG]"
TAG_DATA = "[DAT]"
TAG_IMAGE = "[IMG]"
SERIAL_WRAP_START = "{[(==>"
SERIAL_WRAP_END = "<==]}"

log = logging.getLogger(APP_NAME)

def run_command(cmd=""):
    import subprocess
    import os

    # 创建一个环境变量副本
    env = os.environ.copy()
    # 设置 TERM 为 dumb，来去除颜色输出
    env['TERM'] = 'dumb'

    log.debug("运行命令: %s" % cmd)
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    log.debug("运行命令: 状态: %s" % status)
    log.debug("运行命令: 结果: %s" % result)
    return status, result

# Get the Wi-Fi MAC address
def get_wifi_mac_address():
    import subprocess
    try:
        output = subprocess.check_output(["cat", "/sys/class/net/wlan0/address"])
        mac_address = output.decode("utf-8").strip()
        return mac_address
    except subprocess.CalledProcessError as e:
        print("Error: Could not get WiFi MAC address.")
        return None

def get_ap_name():
    import os
    # mac = get_wifi_mac_address()
    # mac = mac.replace(":", "")
    # mac = mac[:6]
    # return f"{AP_NAME_PREFIX}{mac}"
    if not os.path.exists(APNAME_FILE):
        return f"None"
    with open(APNAME_FILE, 'r') as f:
        ap_name = f.read().strip()
        return ap_name

def set_ap_name(ap_name):
    with open(APNAME_FILE, 'w') as f:
        f.write(ap_name)

def light_led(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.01)

def play_music(file):
    run_command(f"sudo pulseaudio --k")
    run_command(f"sudo pulseaudio --start")
    run_command(f"aplay {file}")

class SerialTestDaemon():

    PORT = '/dev/ttyS0'  # Linux 下的串口名
    BAUDRATE = 115200

    # 0-100-0 iters
    ITER_0_100_0 = list(range(101))
    ITER_0_100_0 += list(range(100, 0, -1))

    def __init__(self):
        # 用于控制是否持续发送传感器数据
        self.ser= None
        self.sensor_datas = {}
        self.sensor_thread = None
        self.sensor_data_start = False
        self.bella = Bella()
        self.bella.motors.reverse([True, False])
        self.strip = PixelStrip(32, 10, 1000000, 10, False, 50)
        self.strip.begin()
        
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
        console_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        log.addHandler(file_handler)
        log.addHandler(console_handler)

        self.send_lock = False

    def send(self, tag, msg):
        if self.send_lock:
            return
        log.debug("发送数据: %s %s" % (tag, msg))

        if self.ser:
            self.send_lock = True
            tmp = SERIAL_WRAP_START + tag + msg + SERIAL_WRAP_END
            self.ser.write(tmp.encode(ENCODING))
            self.ser.flush()
            self.send_lock = False

    def send_data(self, data):
        self.send(TAG_DATA, data)
        # self.send(TAG_DATA, data.encode(ENCODING))

    def send_log(self, msg):
        self.send(TAG_LOG, msg)
        # self.send(TAG_LOG, msg.encode(ENCODING))

    def send_image(self, image_data):
        self.send(TAG_IMAGE, image_data)

    def handle_test_motor(self):
        self.send_log("测试电机")

        delay_time = 0.01
        # 前进
        self.send_log("前进")
        for i in self.ITER_0_100_0:
            self.bella.motors.forward(i)
            time.sleep(delay_time)
        # 后退
        self.send_log("后退")
        for i in self.ITER_0_100_0:
            self.bella.motors.backward(i)
            time.sleep(delay_time)
        # 左转
        self.send_log("左转")
        for i in self.ITER_0_100_0:
            self.bella.motors.turn_left(i)
            time.sleep(delay_time)
        # 右转
        self.send_log("右转")
        for i in self.ITER_0_100_0:
            self.bella.motors.turn_right(i)
            time.sleep(delay_time)
        # 停止
        self.send_log("停止")
        self.bella.motors.stop()

    def handle_test_fan(self):
        self.send_log("测试风扇")
        # 开启风扇
        self.send_log("开启风扇")
        self.bella.fan_on()
        time.sleep(2)
        # 关闭风扇
        self.send_log("关闭风扇")
        self.bella.fan_off()

    def handle_record_play(self):
        self.send_log("录音3秒后，播放录音")
        # 录音
        run_command(f"sudo pulseaudio --k")
        run_command(f"sudo pulseaudio --start")
        self.send_log("录音3秒开始")
        status, result = run_command(f"arecord -d 3 -f S16_LE -r 44100 {TEST_RECORD_FILE}")
        if status != 0:
            self.send_log(f"录音失败: {result}")
            return
        # 播放录音
        self.send_log("播放录音")
        status, result = run_command(f"aplay {TEST_RECORD_FILE}")
        if status != 0:
            self.send_log(f"播放失败: {result}")
            return

    def handle_test_music(self):
        # 播放音乐
        self.send_log("播放音乐")
        play_music(TEST_MUSIC_FILE)

    def handle_test_led(self):
        self.send_log("测试灯环")

        delay_time = 0.5
        # 灯环测试
        self.send_log("红")
        light_led(self.strip, Color(255, 0, 0))
        time.sleep(delay_time)
        self.send_log("绿")
        light_led(self.strip, Color(0, 255, 0))
        time.sleep(delay_time)
        self.send_log("蓝")
        light_led(self.strip, Color(0, 0, 255))
        time.sleep(delay_time)
        self.send_log("白")
        light_led(self.strip, Color(255, 255, 255))
        time.sleep(delay_time)
        self.send_log("停止")
        light_led(self.strip, Color(0, 0, 0))

    def handle_test_camera(self):
        # 摄像头测试
        # self.send_log("测试相机连接")
        # status, result = run_command("libcamera-raw")
        # self.send_log(result)
        # if status == 0:
        #     self.send_log("相机正常")
        # else:
        #     self.send_log("相机异常")
        self.send_log("测试相机")
        self.send_log("拍照")
        status, result = run_command(f"rpicam-jpeg -n --width {TEST_IMAGE_WIDTH} --height {TEST_IMAGE_HEIGHT} --rotation {TEST_IMAGE_ROTATION} -o {TEST_IMAGE_FILE}")
        if status != 0:
            self.send_log(f"拍照失败: {result}")
        else:
            self.send_log("发送图片")
            with open(TEST_IMAGE_FILE, 'rb') as file:
                image_data = file.read()
            self.send_log("完成")

            import base64
            image_data = base64.b64encode(image_data).decode(ENCODING)

            self.send_image(image_data)

    def handle_test_life(self):
        self.send_log("测试老化电机和风扇")
        self.bella.motors.forward(100)
        self.bella.fan_on()

    def update_sensor_data(self):
        while self.sensor_data_start:
            data = {
                "battery_voltage": self.bella.get_battery_voltage(),
                "battery_percentage": self.bella.get_battery_percentage(),
                "charging_state": self.bella.read_charge_status(),
                "ultrasonic_distance": self.bella.get_ultrasonic_distance(),
                "temperature": self.bella.get_temperature(),
                "humidity": self.bella.get_humidity(),
                "grayscale": self.bella.get_grayscales(),
                "btn_state": self.bella.read_btn(),
                "acc": self.bella.get_acc(),
                "gyro": self.bella.get_gyro(),
                "motor_speed": self.bella.motors.speed(),
                "fan_state": self.bella.fan_state,
                "wifi_ap_name": get_ap_name(),
            }

            self.send_data(json.dumps(data))
            time.sleep(1)

    def handle_start_data_send(self):
        log.debug("开始发送传感器数据")
        if self.sensor_data_start == False:
            self.sensor_data_start = True
            self.sensor_thread = threading.Thread(target=self.update_sensor_data, daemon=True)
            self.sensor_thread.start()
        else:
            self.send_log("测试指令已开始")

    def handle_set_ap_name(self, ap_name):
        self.send_log(f"设置 AP 名称: {ap_name}")
        set_ap_name(ap_name)
        self.send_log("设置完成")

    def process_command(self, command):
        if command == "数据开":
            self.handle_start_data_send()
        elif command == "数据关":
            self.send_log("停止发送数据")
            self.sensor_data_start = False
            self.sensor_thread.join()
            self.sensor_thread = None
        elif command == "电机":
            self.handle_test_motor()
        elif command == "风扇":
            self.handle_test_fan()
        elif command == "录播":
            self.handle_record_play()
        elif command == "喇叭":
            self.handle_test_music()
        elif command == "灯":
            self.handle_test_led()
        elif command == "相机":
            self.handle_test_camera()
        elif command == "老化":
            self.handle_test_life()
        elif command.startswith("AP"):
            self.handle_set_ap_name(command.split(':')[1])
        else:
            self.send_log("未知指令")

    def main(self):
        play_music(FACTORY_MODE_AUDIO)
        time.sleep(1)

        try:
            self.ser = serial.Serial(self.PORT, self.BAUDRATE, timeout=1)

            self.handle_start_data_send()
            log.info(f"串口 {self.PORT} 已打开，波特率为 {self.BAUDRATE}")

            while True:
                if self.ser.in_waiting == 0:
                    continue
                try:
                    data = self.ser.readline().decode(ENCODING).strip()
                except UnicodeDecodeError as e:
                    log.warning(f"接收到非法数据: {e}")
                log.debug(f"接收到指令: {data}")
                self.process_command(data)
                self.ser.reset_input_buffer()
                time.sleep(1)
        except serial.SerialException as e:
            log.error(f"串口错误: {e}")
        except KeyboardInterrupt:
            log.info("程序已终止")
        finally:
            if self.ser:
                self.ser.close()


if __name__ == "__main__":
    app = SerialTestDaemon()
    app.main()
