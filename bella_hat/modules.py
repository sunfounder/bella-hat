#!/usr/bin/env python3
from .pin import Pin
from .pwm import PWM
from .adc import ADC
from .i2c import I2C
import time
from .basic import _Basic_class
from typing import Union, List, Tuple, Optional
from gpiozero import OutputDevice, InputDevice

class Ultrasonic():
    SOUND_SPEED = 343.3 # ms

    def __init__(self, trig, echo, timeout=0.02):
        if not isinstance(trig, Pin):
            raise TypeError("trig must be bella_hat.Pin object")
        if not isinstance(echo, Pin):
            raise TypeError("echo must be bella_hat.Pin object")

        self.timeout = timeout

        trig.close()
        echo.close()
        self.trig = Pin(trig._pin_num)
        self.echo = Pin(echo._pin_num, mode=Pin.IN, pull=Pin.PULL_DOWN)

    def _read(self):
        self.trig.off()
        time.sleep(0.001)
        self.trig.on()
        time.sleep(0.00001)
        self.trig.off()

        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()

        while self.echo.gpio.value == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.gpio.value == 1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        if pulse_start == 0 or pulse_end == 0:
            return -2

        during = pulse_end - pulse_start
        cm = round(during * self.SOUND_SPEED / 2 * 100, 2)
        return cm

    def read(self, times=10):
        for i in range(times):
            a = self._read()
            if a != -1:
                return a
        return -1

class ADXL345(I2C):
    """ADXL345 modules"""

    X = 0
    """X"""
    Y = 1
    """Y"""
    Z = 2
    """Z"""
    ADDR =  0x53
    _REG_DATA_X = 0x32  # X-axis data 0 (6 bytes for X/Y/Z)
    _REG_DATA_Y = 0x34  # Y-axis data 0 (6 bytes for X/Y/Z)
    _REG_DATA_Z = 0x36  # Z-axis data 0 (6 bytes for X/Y/Z)
    _REG_POWER_CTL = 0x2D  # Power-saving features control
    _AXISES = [_REG_DATA_X, _REG_DATA_Y, _REG_DATA_Z]

    def __init__(self, *args, address: int = ADDR, bus: int = 1, **kwargs):
        """
        Initialize ADXL345

        :param address: address of the ADXL345
        :type address: int
        """
        super().__init__(address=address, bus=bus, *args, **kwargs)
        self.address = address

    def read(self, axis: int = None) -> Union[float, List[float]]:
        """
        Read an axis from ADXL345

        :param axis: read value(g) of an axis, ADXL345.X, ADXL345.Y or ADXL345.Z, None for all axis
        :type axis: int
        :return: value of the axis, or list of all axis
        :rtype: float/list
        """
        if axis is None:
            return [self._read(i) for i in range(3)]
        else:
            return self._read(axis)

    def _read(self, axis: int) -> float:
        raw_2 = 0
        result = super().read()
        data = (0x08 << 8) + self._REG_POWER_CTL
        if result:
            self.write(data)
        self.mem_write(0, 0x31)
        self.mem_write(8, 0x2D)
        raw = self.mem_read(2, self._AXISES[axis])

        # the first value is always 0, so read it once more
        self.mem_write(0, 0x31)
        self.mem_write(8, 0x2D)
        raw = self.mem_read(2, self._AXISES[axis])
        if raw[1] >> 7 == 1:
            raw_1 = raw[1] ^ 128 ^ 127
            raw_2 = (raw_1 + 1) * -1
        else:
            raw_2 = raw[1]
        g = raw_2 << 8 | raw[0]
        value = g / 256.0
        return value


class RGB_LED():
    """Simple 3 pin RGB LED"""

    ANODE = 1
    """Common anode"""
    CATHODE = 0
    """Common cathode"""

    def __init__(self, r_pin: PWM, g_pin: PWM, b_pin: PWM, common: int = 1):
        """
        Initialize RGB LED

        :param r_pin: PWM object for red
        :type r_pin: bella_hat.PWM
        :param g_pin: PWM object for green
        :type g_pin: bella_hat.PWM
        :param b_pin: PWM object for blue
        :type b_pin: bella_hat.PWM
        :param common: RGB_LED.ANODE or RGB_LED.CATHODE, default is ANODE
        :type common: int
        :raise ValueError: if common is not ANODE or CATHODE
        :raise TypeError: if r_pin, g_pin or b_pin is not PWM object
        """
        if not isinstance(r_pin, PWM):
            raise TypeError("r_pin must be bella_hat.PWM object")
        if not isinstance(g_pin, PWM):
            raise TypeError("g_pin must be bella_hat.PWM object")
        if not isinstance(b_pin, PWM):
            raise TypeError("b_pin must be bella_hat.PWM object")
        if common not in (self.ANODE, self.CATHODE):
            raise ValueError("common must be RGB_LED.ANODE or RGB_LED.CATHODE")
        self.r_pin = r_pin
        self.g_pin = g_pin
        self.b_pin = b_pin
        self.common = common

    def color(self, color: Union[str, Tuple[int, int, int], List[int], int]):
        """
        Write color to RGB LED

        :param color: color to write, hex string starts with "#", 24-bit int or tuple of (red, green, blue)
        :type color: str/int/tuple/list
        """
        if not isinstance(color, (str, int, tuple, list)):
            raise TypeError("color must be str, int, tuple or list")
        if isinstance(color, str):
            color = color.strip("#")
            color = int(color, 16)
        if isinstance(color, (tuple, list)):
            r, g, b = color
        if isinstance(color, int):
            r = (color & 0xff0000) >> 16
            g = (color & 0x00ff00) >> 8
            b = (color & 0x0000ff) >> 0

        if self.common == self.ANODE:
            r = 255-r
            g = 255-g
            b = 255-b

        r = r / 255.0 * 100.0
        g = g / 255.0 * 100.0
        b = b / 255.0 * 100.0

        self.r_pin.pulse_width_percent(r)
        self.g_pin.pulse_width_percent(g)
        self.b_pin.pulse_width_percent(b)


class Buzzer():
    """Buzzer"""

    def __init__(self, buzzer: Union[PWM, Pin]):
        """
        Initialize buzzer

        :param pwm: PWM object for passive buzzer or Pin object for active buzzer
        :type pwm: bella_hat.PWM/bella_hat.Pin
        """
        if not isinstance(buzzer, (PWM, Pin)):
            raise TypeError(
                "buzzer must be bella_hat.PWM or bella_hat.Pin object")
        self.buzzer = buzzer
        self.buzzer.off()

    def on(self):
        """Turn on buzzer"""
        if isinstance(self.buzzer, PWM):
            self.buzzer.pulse_width_percent(50)
        elif isinstance(self.buzzer, Pin):
            self.buzzer.on()

    def off(self):
        """Turn off buzzer"""
        if isinstance(self.buzzer, PWM):
            self.buzzer.pulse_width_percent(0)
        elif isinstance(self.buzzer, Pin):
            self.buzzer.off()

    def freq(self, freq: float):
        """Set frequency of passive buzzer

        :param freq: frequency of buzzer, use Music.NOTES to get frequency of note
        :type freq: int/float
        :raise TypeError: if set to active buzzer
        """
        if isinstance(self.buzzer, Pin):
            raise TypeError("freq is not supported for active buzzer")
        self.buzzer.freq(freq)

    def play(self, freq: float, duration: float = None):
        """
        Play freq

        :param freq: freq to play, you can use Music.note() to get frequency of note
        :type freq: float
        :param duration: duration of each note, in seconds, None means play continuously
        :type duration: float
        :raise TypeError: if set to active buzzer
        """
        if isinstance(self.buzzer, Pin):
            raise TypeError("play is not supported for active buzzer")
        self.freq(freq)
        self.on()
        if duration is not None:
            time.sleep(duration/2)
            self.off()
            time.sleep(duration/2)


class Grayscale_Module(object):
    """3 channel Grayscale Module"""

    LEFT = 0
    """Left Channel"""
    MIDDLE = 1
    """Middle Channel"""
    RIGHT = 2
    """Right Channel"""

    REFERENCE_DEFAULT = [1000]*3

    def __init__(self, pin0: ADC, pin1: ADC, pin2: ADC, reference: int = None):
        """
        Initialize Grayscale Module

        :param pin0: ADC object or int for channel 0
        :type pin0: bella_hat.ADC/int
        :param pin1: ADC object or int for channel 1
        :type pin1: bella_hat.ADC/int
        :param pin2: ADC object or int for channel 2
        :type pin2: bella_hat.ADC/int
        :param reference: reference voltage
        :type reference: 1*3 list, [int, int, int]
        """
        self.pins = (pin0, pin1, pin2)
        for i, pin in enumerate(self.pins):
            if not isinstance(pin, ADC):
                raise TypeError(f"pin{i} must be bella_hat.ADC")
        self._reference = self.REFERENCE_DEFAULT

    def reference(self, ref: list = None) -> list:
        """
        Get Set reference value

        :param ref: reference value, None to get reference value
        :type ref: list
        :return: reference value
        :rtype: list
        """
        if ref is not None:
            if isinstance(ref, list) and len(ref) == 3:
                self._reference = ref
            else:
                raise TypeError("ref parameter must be 1*3 list.")
        return self._reference

    def read_status(self, datas: list = None) -> list:
        """
        Read line status

        :param datas: list of grayscale datas, if None, read from sensor
        :type datas: list
        :return: list of line status, 0 for white, 1 for black
        :rtype: list
        """
        if self._reference == None:
            raise ValueError("Reference value is not set")
        if datas == None:
            datas = self.read()
        return [0 if data > self._reference[i] else 1 for i, data in enumerate(datas)]

    def read(self, channel: int = None) -> list:
        """
        read a channel or all datas

        :param channel: channel to read, leave empty to read all. 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT 
        :type channel: int/None
        :return: list of grayscale data
        :rtype: list
        """
        if channel == None:
            return [self.pins[i].read() for i in range(3)]
        else:
            return self.pins[channel].read()

class DHT11():

    def __init__(self, pin):
        import board
        import adafruit_dht

        _pin = getattr(board, f"D{pin}")
        self.dht11 = adafruit_dht.DHT11(_pin, use_pulseio=False)

    @property
    def temperature(self):
        try:
            return self.dht11.temperature
        except:
            return 0.0

    @property
    def humidity(self):
        try:
            return self.dht11.humidity
        except:
            return 0

# class DHT11():
#     MAX_DELAY_COUINT = 100
#     BIT_1_DELAY_COUNT = 10
#     BITS_LEN = 40
#     TIMEOUT = 2 # seconds

#     def __init__(self, pin, pull_up=False):
#         self._pin = pin
#         self._pull_up = pull_up

#     def read_data(self):
#         bit_count = 0
#         delay_count = 0
#         bits = ""

#         # -------------- send start --------------
#         gpio = OutputDevice(self._pin)
#         gpio.off()
#         time.sleep(0.02)

#         gpio.close()
#         gpio = InputDevice(self._pin, pull_up=self._pull_up)

#         # -------------- wait response --------------
#         st = time.time()
#         while gpio.value == 1:
#             if time.time() - st > self.TIMEOUT:
#                 raise TimeoutError("Timeout. Please check the wiring.")
        
#         # -------------- read data --------------
#         while bit_count < self.BITS_LEN:
#             st = time.time()
#             while gpio.value == 0:
#                 if time.time() - st > self.TIMEOUT:
#                     raise TimeoutError("Timeout. Please check the wiring.")

#             # st = time.time()
#             while gpio.value == 1:
#                 delay_count += 1
#                 # break
#                 if delay_count > self.MAX_DELAY_COUINT:
#                     break
#             if delay_count > self.BIT_1_DELAY_COUNT:
#                 bits += "1"
#             else:
#                 bits += "0"

#             delay_count = 0
#             bit_count += 1

#         # -------------- verify --------------
#         humidity_integer = int(bits[0:8], 2)
#         humidity_decimal = int(bits[8:16], 2)
#         temperature_integer = int(bits[16:24], 2)
#         temperature_decimal = int(bits[24:32], 2)
#         check_sum = int(bits[32:40], 2)

#         _sum = humidity_integer + humidity_decimal + temperature_integer + temperature_decimal

#         # print(bits)
#         # print(humidity_integer, humidity_decimal, temperature_integer, temperature_decimal)
#         # print(f'sum:{_sum}, check_sum:{check_sum}')
#         # print()

#         if check_sum != _sum:
#             humidity = None
#             temperature = None
#         else:
#             humidity = float(f'{humidity_integer}.{humidity_decimal}')
#             temperature = float(f'{temperature_integer}.{temperature_decimal}')

#         # -------------- return --------------
#         return humidity, temperature

class LSM6DSOX():

    def __init__(self):
        import board
        from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

        _i2c = board.I2C()
        self.lsm6dsox = LSM6DSOX(_i2c)

    @property
    def acc(self):
        return self.lsm6dsox.acceleration

    @property
    def gyro(self):
        return self.lsm6dsox.gyro

