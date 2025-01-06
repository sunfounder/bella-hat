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
# Run the following command in the terminal to start factory test:
# python3 bella-factory-test.py
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
# AP:WIFIXXX    设置AP为WIFI:T:WPA;S:bella-876zyx;P:87654321;;
# 灰度白        校准灰度白色
# 灰度黑        校准灰度黑色

import serial
import threading
import time
import os
import logging
import subprocess
import select
import json
from logging.handlers import RotatingFileHandler

from bella_hat.bella import Bella
from rpi_ws281x import PixelStrip, Color

APP_NAME = 'bella-factory-test'
ENCODING = 'utf-8'
TEST_FOLDER = f'/opt/{APP_NAME}'
TEST_MUSIC_FILE = f'{TEST_FOLDER}/test_music.wav'
TEST_RECORD_FILE = f'{TEST_FOLDER}/test_record.wav'
TEST_IMAGE_FILE = f'{TEST_FOLDER}/test_image.jpg'
FACTORY_MODE_AUDIO = f'{TEST_FOLDER}/factory-mode.wav'
FIRST_BOOT_FLAG = f'{TEST_FOLDER}/firstboot'
AP_CONFIG_FILE = f'/etc/bella-ap.conf'
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

def run_command(cmd="", timeout=None):
    # 创建一个环境变量副本
    env = os.environ.copy()
    # 设置 TERM 为 dumb，来去除颜色输出
    env['TERM'] = 'dumb'

    log = logging.getLogger()  # 确保你有 logger 可用
    log.debug("运行命令: %s" % cmd)

    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True)

    temp_output = ""  # 中间结果暂存输出
    try:
        if timeout is None:
            temp_output, _ = p.communicate()  # 不设置超时
        else:
            end_time = time.time() + timeout
            while True:
                rlist, _, _ = select.select([p.stdout], [], [], timeout)
                if rlist:
                    line = p.stdout.readline()
                    if not line:
                        break
                    temp_output += line  # 将输出逐行添加到 temp_output 中
                if time.time() > end_time:
                    p.kill()  # 超时后强制结束进程
                    temp_output += '拍照超时\n'  # 追加超时信息
                    break
                    
        status = p.poll()
    except Exception as e:
        log.error("运行命令时出现异常: %s" % str(e))
        status = -1  # 错误状态码
        temp_output += f"Error: {str(e)}\n"  # 追加错误信息

    log.debug("运行命令: 状态: %s" % (status if status is not None else -1))
    log.debug("运行命令: 结果: %s" % temp_output)
    return (status if status is not None else -1), temp_output

# def run_command(cmd=""):
#     import subprocess
#     import os

#     # 创建一个环境变量副本
#     env = os.environ.copy()
#     # 设置 TERM 为 dumb，来去除颜色输出
#     env['TERM'] = 'dumb'

#     log.debug("运行命令: %s" % cmd)
#     p = subprocess.Popen(
#         cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
#     result = p.stdout.read().decode('utf-8')
#     status = p.poll()
#     log.debug("运行命令: 状态: %s" % status)
#     log.debug("运行命令: 结果: %s" % result)
#     return status, result

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

def get_ap():
    import os
    result = {}
    if not os.path.exists(AP_CONFIG_FILE):
        return f"None"
    with open(AP_CONFIG_FILE, 'r') as f:
        config = f.read().strip()
        if not config:
            return f"None"
        ssid = config.split('\n')[0].split('=')[1].strip()
        password = config.split('\n')[1].split('=')[1].strip()
        result = {
            "ssid": ssid,
            "password": password
        }
        return result

def set_ap(ssid, password):
    contect = f"BELLA_SSID={ssid}\nBELLA_PASSWORD={password}\n"
    with open(AP_CONFIG_FILE, 'w') as f:
        f.write(contect)
    run_command(f"sudo systemctl restart bella-ap")

def set_hostname(hostname):
    run_command(f"sudo hostnamectl set-hostname {hostname}")

def light_led(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.01)

def get_disk_size():
    _, result = run_command("lsblk | grep mmcblk0 | awk '{print $4}'")
    result = result.strip().split('\n')
    return result

def play_music(file):
    run_command(f"sudo pulseaudio --k")
    run_command(f"sudo pulseaudio --start")
    run_command(f"aplay {file}")

class FactoryTest():

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

        self.grayscale_white = None
        self.grayscale_black = None
        self.life_test_started = False

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
        status, result = run_command(f"rpicam-jpeg -n --width {TEST_IMAGE_WIDTH} --height {TEST_IMAGE_HEIGHT} --rotation {TEST_IMAGE_ROTATION} -o {TEST_IMAGE_FILE}", 10)
        if status != 0:
            self.send_log(f"拍照失败: {result}")
        else:
            self.send_log("发送图片")
            with open(TEST_IMAGE_FILE, 'rb') as file:
                image_data = file.read()

            import base64
            image_data = base64.b64encode(image_data).decode(ENCODING)

            self.send_image(image_data)
            self.send_log("完成")
            os.remove(TEST_IMAGE_FILE)

    def handle_test_life(self):
        if self.life_test_started:
            self.send_log("停止老化测试")
            self.bella.motors.stop()
            self.bella.fan_off()
            self.life_test_started = False
        else:
            self.send_log("测试老化电机和风扇")
            self.bella.motors.forward(100)
            self.bella.fan_on()
            self.life_test_started = True

    def get_grayscale_avg(self, times=10):
        grayscale_datas = []
        for _ in range(10):
            grayscale_data = self.bella.get_grayscales(raw=True)
            grayscale_datas.append(grayscale_data)
            time.sleep(0.1)
        avg_grayscale_data = [0, 0, 0]
        for grayscale_data in grayscale_datas:
            avg_grayscale_data[0] += grayscale_data[0]
            avg_grayscale_data[1] += grayscale_data[1]
            avg_grayscale_data[2] += grayscale_data[2]
        avg_grayscale_data[0] /= len(grayscale_datas)
        avg_grayscale_data[1] /= len(grayscale_datas)
        avg_grayscale_data[2] /= len(grayscale_datas)
        return avg_grayscale_data

    def handle_grayscale_calibrate_white(self):
        self.send_log("灰度校准白色")
        self.grayscale_white = self.get_grayscale_avg()
        self.send_log(f"白色灰度值: {self.grayscale_white}")
        self.handle_grayscale_calibrate()

    def handle_grayscale_calibrate_black(self):
        self.send_log("灰度校准黑色")
        self.grayscale_black = self.get_grayscale_avg()
        self.send_log(f"黑色灰度值: {self.grayscale_black}")
        self.handle_grayscale_calibrate()

    def handle_grayscale_calibrate(self):
        if self.grayscale_white is None or self.grayscale_black is None:
            return
        # 找到读取值最大的传感器编号
        max_grayscale = max(self.grayscale_white)
        max_index = self.grayscale_white.index(max_grayscale)
        # 计算另外两个传感器和最大值的线性方程参数 y=ax+b
        slopes = [] # 斜率
        offsets = [] # 截距
        for i in range(3):
            if i == max_index:
                slopes.append(1)
                offsets.append(0)
            else:
                x1 = self.grayscale_black[i]
                y1 = self.grayscale_black[max_index]
                x2 = self.grayscale_white[i]
                y2 = self.grayscale_white[max_index]
                if x2 - x1 == 0 or y2 - y1 == 0:
                    self.send_log(f"校准失败: 黑和白的值相等。白：{self.grayscale_white}，黑：{self.grayscale_black}")
                    return
                if x2 - x1 < 0 or y2 - y1 < 0:
                    self.send_log(f"校准失败: 黑的值应该小于白的值。白：{self.grayscale_white}，黑：{self.grayscale_black}")
                    return
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1
                slopes.append(round(a, 2))
                offsets.append(round(b, 2))
        # 设置校准参数
        self.bella.set_grayscale_calibration(slopes, offsets)
        self.send_log(f"灰度校准完成: {slopes}, {offsets}")

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
                "ap_config": get_ap(),
                "disk_size": get_disk_size(),
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

    def handle_set_ap(self, config):
        # WIFI:T:WPA;S:bella-876zyx;P:87654321;;
        # 取出 ssid 和 password
        ap_ssid = ""
        ap_password = ""
        if not config.startswith("WIFI:"):
            self.send_log(f"设置 AP 失败: 配置格式错误。")
            return
        config = config.replace("WIFI:", "")
        items = config.split(';')
        for item in items:
            if item.startswith("S:"):
                ap_ssid = item.split(':')[1]
            elif item.startswith("P:"):
                ap_password = item.split(':')[1]
        if not ap_ssid or not ap_password or len(ap_ssid) > 32 or len(ap_password) > 64 \
            or len(ap_ssid) < 1 or len(ap_password) < 8:
            self.send_log(f"设置 AP 失败: 配置格式错误。")
            return
        self.send_log(f"设置 AP 名称: {ap_ssid}  密码: {ap_password}")
        set_ap(ap_ssid, ap_password)
        set_hostname(ap_ssid)
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
            self.handle_set_ap(command.split('AP:')[1])
        elif command.startswith("灰度白"):
            self.handle_grayscale_calibrate_white()
        elif command.startswith("灰度黑"):
            self.handle_grayscale_calibrate_black()
        else:
            self.send_log(f"未知指令: {command}")

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
    app = FactoryTest()
    app.main()
