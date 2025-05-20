# Setup 
#
# Disable Serial Console and enable Serial Port
# sudo raspi-config
# Interfacing Options -> Serial -> No -> Yes
# 
# Reboot the Raspberry Pi
#
# Port: /dev/ttyS0
# Baudrate: 460800
#
# Run the following command in the terminal to start factory test:
# python3 bella-factory-test.py
#
# The test commands are sent through the serial port. 
# Each sending needs to end with "\n".
#
# data_on                    start sending sensor data
# data_off                   stop sending sensor data
# aging                      test motor fan, aging
# motor                      test motor, car forward, speed slowly increase and decrease, then backward, speed slowly increase and decrease, then stop, then turn left, turn right, stop
# fan                        test fan, fan on 2 seconds, fan off 2 seconds
# record_play                record 3 seconds, play record
# play                       play music
# rgb_led                    test rgb_led, red, green, blue, white, then stop
# camera                     take a photo and return base64 format image
# ap:<WIFI_CONFIG>           set AP to WIFI:T:WPA;S:bella-876zyx;P:87654321;;
# white                      calibrate grayscale module white
# black                      calibrate  grayscale module black
# auto_factory_mode:<STATE>  1:enable auto factory mode, 0:disable auto factory mode
# sn:<SERIAL_NUMBER>         set serial number(batch number) to x; 

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
FACTORY_MODE_AUDIO = f'{TEST_FOLDER}/factory-mode2.wav'
ERROR_AUDIO = f'{TEST_FOLDER}/run_error.wav'
RUN_END_AUDIO = f'{TEST_FOLDER}/run_end.wav'
CAM_INIT_ERROR_AUDIO = f'{TEST_FOLDER}/cam_init_error.wav'
ENABLIED_AUTO_FACTORY_MODE = f'{TEST_FOLDER}/enable_auto_factory_mode.wav'
DISABLED_AUTO_FACTORY_MODE = f'{TEST_FOLDER}/disable_auto_factory_mode.wav'
EXIT_AUDIO = f'{TEST_FOLDER}/exit.wav'
FIRST_BOOT_FLAG = f'{TEST_FOLDER}/firstboot'
AP_CONFIG_FILE = f'/etc/bella-ap.conf'
AUTO_FACTORY_MODE='/boot/firmware/bella-auto-factory-mode'
SERIAL_NUMBER_FILE = f'/opt/bella/sn'  
TEST_IMAGE_WIDTH = 800
TEST_IMAGE_HEIGHT = 600
TEST_IMAGE_HLIP = False
TEST_IMAGE_VLIP = True

LOG_FILE = f'/var/log/{APP_NAME}.log'

PORT = '/dev/ttyS0'  # Linux Serial Port
BAUDRATE = 460800
# BAUDRATE = 115200

SERIAL_EVENT_INTERVAL = 1
KEY_EVENT_INTERVAL = 0.05

capture_config = None
picam2 = None

TAG_LOG = "[LOG]"
TAG_DATA = "[DAT]"
TAG_IMAGE = "[IMG]"
SERIAL_WRAP_START = "{[(==>"
SERIAL_WRAP_END = "<==]}"


ap_config = None
sn = None


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
        f.flush()
        os.fsync(f.fileno())

    # read config again
    global ap_config
    ap_config = get_ap()
    #
    run_command(f"sudo systemctl restart bella-ap")

def set_hostname(hostname):
    _, old_hostname = run_command("hostname")
    old_hostname = old_hostname.strip()
    if old_hostname == hostname:
        return
    run_command(f"sudo hostnamectl set-hostname {hostname}")
    with open('/etc/hosts', 'r') as f:
        content = f.read()
    content = content.replace(old_hostname, hostname)
    with open('/etc/hosts', 'w') as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())

def get_sn():
    import os
    if not os.path.exists(SERIAL_NUMBER_FILE):
        return f"None"
    with open(SERIAL_NUMBER_FILE, 'r') as f:
        serial_number = f.read().strip()
        if not serial_number:
            return f"None"
        else:
            return serial_number

def set_serial_number(serial_number):
    import os
    if not os.path.exists(SERIAL_NUMBER_FILE):
        os.makedirs(os.path.dirname(SERIAL_NUMBER_FILE), exist_ok=True)
    with open(SERIAL_NUMBER_FILE, 'w') as f:
        f.write(serial_number)
        f.flush()
        os.fsync(f.fileno())
    # read sn again
    global sn
    sn = get_sn()

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
    # run_command(f"sudo pulseaudio --k")
    # run_command(f"sudo pulseaudio --start")
    run_command(f"aplay {file}")

class FactoryTest():

    # 0-100-0 iters
    ITER_0_100_0 = list(range(101))
    ITER_0_100_0 += list(range(100, 0, -1))
    auto_factory_mode = False
    
    def __init__(self):
        # Whether to continuously send sensor data
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

        self.auto_factory_mode = os.path.exists(AUTO_FACTORY_MODE)

        self.send_lock = False

        self.grayscale_white = None
        self.grayscale_black = None
        self.life_test_started = False

        self.key_press_time_count = 0

        # turn up volumn
        run_command(f"amixer set 'Speaker' 100%")
        run_command(f"amixer set 'Mic' 100%")

    def send(self, tag, msg):
        if self.send_lock:
            return
        log.debug("发送数据: %s %s" % (tag, msg))

        try:
            if self.ser:
                self.send_lock = True
                tmp = SERIAL_WRAP_START + tag + msg + SERIAL_WRAP_END
                self.ser.write(tmp.encode(ENCODING))
                self.ser.flush()
                self.send_lock = False
        except Exception as e:
            log.error(f"串口出错 {e}")

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
        self.send_log("测试相机")
        self.send_log("拍照")

        try:
            picam2.switch_mode_and_capture_file(capture_config, TEST_IMAGE_FILE)
        except Exception as e:
            log.error(f"拍照失败: {str(e)}")
            self.send_log(f"拍照失败: {str(e)}")
            return

        self.send_log("发送图片")
        with open(TEST_IMAGE_FILE, 'rb') as file:
            image_data = file.read()

        import base64
        image_data = base64.b64encode(image_data).decode(ENCODING)

        self.send_image(image_data)
        self.send_log("完成")
        os.remove(TEST_IMAGE_FILE)
        os.sync()

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
        g0_datas = []
        g1_datas = []
        g2_datas = []

        for _ in range(10):
            g0, g1, g2 = self.bella.get_grayscales(raw=True)
            g0_datas.append(g0)
            g1_datas.append(g1)
            g2_datas.append(g2)
            time.sleep(0.1)
    
        avg_grayscale_data = [0, 0, 0]

        # 计算平均灰度值
        # g0_sum = 0
        # g1_sum = 0
        # g2_sum = 0
 
        # for i in range(10):
        #     g0_sum += g0_datas[i]
        #     g1_sum += g1_datas[i]
        #     g2_sum += g2_datas[i]

        # avg_grayscale_data[0] = g0_sum / 10
        # avg_grayscale_data[1] = g1_sum / 10
        # avg_grayscale_data[2] = g2_sum / 10

        # return avg_grayscale_data


        # 计算灰度中位数
        g0_datas.sort()
        g1_datas.sort()
        g2_datas.sort()

        avg_grayscale_data[0] = (g0_datas[4] + g0_datas[5]) / 2
        avg_grayscale_data[1] = (g1_datas[4] + g1_datas[5]) / 2
        avg_grayscale_data[2] = (g2_datas[4] + g2_datas[5]) / 2

        return avg_grayscale_data

    def handle_grayscale_calibrate_white(self):
        try:
            self.send_log("灰度校准白色")
            self.grayscale_white = self.get_grayscale_avg()
            self.send_log(f"白色灰度值: {self.grayscale_white}")
            self.handle_grayscale_calibrate()
        except Exception as e:
            self.send_log(f"灰度校准白色失败: {str(e)}")
            self.send_log("请重新校准")

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

    def handle_auto_factory_mode(self, data):
        print(data, type(data))
        if data == "1":
            if self.auto_factory_mode:
                pass
            else:
                with open(AUTO_FACTORY_MODE, "w") as f:
                    f.flush()
                    os.fsync(f.fileno())
                self.auto_factory_mode = True
            log.info("自动工厂模式已开启")
            self.send_log("自动工厂模式已开启")
            play_music(ENABLIED_AUTO_FACTORY_MODE)
            time.sleep(1)
        elif data == "0":
            os.remove(AUTO_FACTORY_MODE)
            os.sync() 
            self.auto_factory_mode = False
            log.info("自动工厂模式已关闭")
            self.send_log("自动工厂模式已关闭")
            play_music(DISABLED_AUTO_FACTORY_MODE)
            time.sleep(1)
        else:
            self.send_log("请输入1或0")

    def handle_serial_number(self, data):
        set_serial_number(data)
        self.send_log(f"序列号已设置为: {data}")
        log.info(f"序列号已设置为: {data}")

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
                "ap_config": ap_config,
                "disk_size": get_disk_size(),
                "auto_factory_mode":self.auto_factory_mode,
                "sn": sn,
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
        # commands = commands.split(';')
        # for command in commands:
        if command == "data_on":
            self.handle_start_data_send()
        elif command == "data_off":
            self.send_log("停止发送数据")
            self.sensor_data_start = False
            self.sensor_thread.join()
            self.sensor_thread = None
        elif command == "motor":
            self.handle_test_motor()
        elif command == "fan":
            self.handle_test_fan()
        elif command == "record_play":
            self.handle_record_play()
        elif command == "play":
            self.handle_test_music()
        elif command == "rgb_led":
            self.handle_test_led()
        elif command == "camera":
            self.handle_test_camera()
        elif command == "aging":
            self.handle_test_life()
        elif command.startswith("ap"):
            self.handle_set_ap(command.split('ap:')[1])
        elif command.startswith("white"):
            self.handle_grayscale_calibrate_white()
        elif command.startswith("black"):
            self.handle_grayscale_calibrate_black()
        elif command.startswith("auto_factory_mode"):
            self.handle_auto_factory_mode(command.split('auto_factory_mode:')[1])
        elif command.startswith("sn"):
            self.handle_serial_number(command.split('sn:')[1])
        else:
            self.send_log(f"unknown command: {command}")


    def key_event_handler(self):
        
        if self.bella.read_btn():
            self.key_press_time_count += KEY_EVENT_INTERVAL
        else:
            self.key_press_time_count = 0

        ## 长按5s 取消自动工厂模式，并且退出
        if self.key_press_time_count >= 5:
            self.key_press_time_count = 0
            #
            if os.path.exists(AUTO_FACTORY_MODE):
                self.auto_factory_mode = False
                os.remove(AUTO_FACTORY_MODE)
                os.sync()
                log.info("取消自动工厂模式")
            # play_music(DISABLED_AUTO_FACTORY_MODE)
            #
            log.info("退出程序")
            play_music(EXIT_AUDIO)
            time.sleep(2)
            if self.ser:
                self.ser.close()
            exit()
            

    def main(self):
        global picam2, capture_config, ap_config, sn 

        play_music(FACTORY_MODE_AUDIO)
        time.sleep(1)
        ## 
        try:
            from picamera2 import Picamera2
            from libcamera import Transform
            picam2 = Picamera2()
            capture_config = picam2.create_still_configuration(
                main={
                    "size": (TEST_IMAGE_WIDTH, TEST_IMAGE_HEIGHT),
                },
                buffer_count=2,
                transform=Transform(hflip=TEST_IMAGE_HLIP, vflip=TEST_IMAGE_VLIP)
            )
            picam2.start()
        except Exception as e:
            log.error(f"初始化相机失败: {e}")
            play_music(CAM_INIT_ERROR_AUDIO)
            time.sleep(1)



        ## read config
        ap_config = get_ap()
        sn = get_sn()

        serial_st = time.time()
        key_st = time.time()

        try:
            self.ser = serial.Serial(PORT, BAUDRATE, timeout=1)

            self.handle_start_data_send()
            log.info(f"串口 {PORT} 已打开，波特率为 {BAUDRATE}")

            while True:

                ## 处理按键事件
                if time.time() - key_st > KEY_EVENT_INTERVAL:
                    key_st = time.time()
                    self.key_event_handler()

                ## 处理串口数据
                if self.ser.in_waiting > 0 and time.time() - serial_st > SERIAL_EVENT_INTERVAL:
                    serial_st = time.time()
                    try:
                        data = self.ser.readline().decode(ENCODING).strip()
                        log.debug(f"接收到指令: {data}")

                    except UnicodeDecodeError as e:
                        log.warning(f"接收到非法数据: {e}")
                        self.send_log(f"接收到非法数据: {e}")
                        data = ""
                    except Exception as e:
                        log.error(f"接收到非法数据: {e}")
                        self.send_log(f"接收到非法数据: {e}")
                        data = ""

                    try:
                        self.process_command(data)
                        self.ser.reset_input_buffer()
                    except Exception as e:
                        log.error(f"处理指令时发生错误: {e}")
                        self.send_log(f"处理指令时发生错误: {e}")
                
                ## loop 间隔
                time.sleep(0.01)
        except serial.SerialException as e:
            log.error(f"串口错误: {e}")
            play_music(ERROR_AUDIO)
            time.sleep(2)
        except KeyboardInterrupt:
            log.info("程序已终止")
            play_music(RUN_END_AUDIO)
            time.sleep(2)
        finally:
            if self.ser:
                self.ser.close()


if __name__ == "__main__":
    app = FactoryTest()
    app.main()
