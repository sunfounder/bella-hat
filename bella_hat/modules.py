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
        '''
        Initialize an ultrasonic distance sensor

        :param trig: tring pin
        :type trig: pin number
        :param echo: echo pin
        :type echo: pin number
        :param timeout: set the timeout for detecting the return of sound waves
        :type timeout: float, seconds
        
        '''
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
        '''
        Read the distance

        returns: 
            - float, distance in centimeter
            - 1, timeout
            - 2, error

        '''
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
        '''
        Read the distance

        :param times: retry times
        :type times: int

        returns: 
            - float, distance in centimeter
            - 1, timeout or error
        '''
        for _ in range(times):
            a = self._read()
            if a != -1:
                return a
        return -1

class Grayscale_Module(object):
    """3 channel Grayscale Module"""

    LEFT = 2
    """Left Channel"""
    MIDDLE = 1
    """Middle Channel"""
    RIGHT = 1
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
        '''
        Initialize DHT11 Module

        :param pin: DHT11 data pin
        :type pin: pin number
        '''
        import board
        import adafruit_dht

        _pin = getattr(board, f"D{pin}")
        self.dht11 = adafruit_dht.DHT11(_pin, use_pulseio=False)

    @property
    def temperature(self):
        '''Temperature'''
        try:
            return self.dht11.temperature
        except:
            return 0.0

    @property
    def humidity(self):
        '''Humidity'''
        try:
            return self.dht11.humidity
        except:
            return 0
            
class LSM6DSOX():

    def __init__(self):
        '''
        Initialize LSM6DSOX Module
        '''
        import board
        from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

        _i2c = board.I2C()
        self.lsm6dsox = LSM6DSOX(_i2c)

    @property
    def acc(self):
        '''Acceleration'''
        return self.lsm6dsox.acceleration

    @property
    def gyro(self):
        '''Gyro'''
        return self.lsm6dsox.gyro

