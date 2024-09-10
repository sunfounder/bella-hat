#!/usr/bin/env python3
from .basic import _Basic_class
from .pwm import PWM

class Motor():
    """Motor"""
    PERIOD = 4095
    PRESCALER = 10

    def __init__(self, pwma, pwmb, reversed=False):
        """
        Initialize a motor

        :param pwma: Motor speed control pwm input A pin
        :type pwm: pin number
        :param pwmb: Motor speed control pwm input B pin
        :type pwmb: pin number
        :reversed: Whether to reverse the direction of motor rotation
        :type reversed: boolean
        """
        self.pwma = PWM(pwma)
        self.pwma.period(self.PERIOD)
        self.pwma.prescaler(self.PRESCALER)
        self.pwma.pulse_width_percent(0)

        self.pwmb = PWM(pwmb)
        self.pwmb.period(self.PERIOD)
        self.pwmb.prescaler(self.PRESCALER)
        self.pwmb.pulse_width_percent(0)

        self._speed = 0
        self._reversed = reversed

    def speed(self, speed=None):
        """
        Get or set motor speed

        :param speed: Motor speed(-100.0~100.0)
        :type speed: int or float 
        """
        # reutn current speed value
        if speed is None:
            return self._speed

        # set motor speed
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100
        self._speed = speed

        dir = 1
        if speed < 0 and self._reversed is False:
                dir = -1
        elif speed > 0 and self._reversed is True:
            dir = -1

        speed = abs(speed)

        if dir == 1:
            self.pwma.pulse_width_percent(speed)
            self.pwmb.pulse_width_percent(0)
        else:
            self.pwma.pulse_width_percent(0)
            self.pwmb.pulse_width_percent(speed)


    def reverse(self, reverse=None):
        """
        Get or set motor is reversed or not

        :param reverse: True or False
        :type reverse: bool
        """
        if reverse is None:
            return self._reversed

        self._reversed = reverse

    def brake(self):
        self.pwma.pulse_width_percent(100)
        self.pwmb.pulse_width_percent(100)

    def stop(self):
        self.pwma.pulse_width_percent(0)
        self.pwmb.pulse_width_percent(0)


class Motors(_Basic_class):
    """Motors"""

    LEFT_MOTOR_PWMA = 18
    LEFT_MOTOR_PWMB = 19
    RIGHT_MOTOR_PWMA = 16
    RIGHT_MOTOR_PWMB = 17
    LEFT_REVERSE = False
    RIGHT_REVERSE = False

    def __init__(self,
                left_motor_pwma=LEFT_MOTOR_PWMA,
                left_motor_pwmb=LEFT_MOTOR_PWMB,
                right_motor_pwma=RIGHT_MOTOR_PWMA,
                right_motor_pwmb=RIGHT_MOTOR_PWMB,
                left_reversed = LEFT_REVERSE,
                right_reversed = RIGHT_REVERSE,
                *args, **kwargs):
        """
        Initialize motors with bella_hat.motor.Motor

        :param db: config file path
        :type db: str
        """
        super().__init__(*args, **kwargs)

        self.left_motor = Motor(left_motor_pwma, left_motor_pwmb, left_reversed)
        self.right_motor = Motor(right_motor_pwma, right_motor_pwmb, right_reversed)

    def stop(self):
        """Stop all motors"""
        self.left_motor.stop()
        self.right_motor.stop()

    def brake(self):
        self.left_motor.brake()
        self.right_motor.brake()

    def reverse(self, reverse=None):
        '''
        Get or set motors is reversed or not

        :param reverse: [left_reverse, right_reverse]
        :type reverse: [bool, bool]
        
        '''
        if reverse is None:
            return [self.left_motor.reverse(), self.right_motor.reverse()]

        if not isinstance(reverse, list):
            raise ValueError('reverse must be a 2*1 list: [left_reverse, right_reverse]')
        elif len(reverse) != 2:
            raise ValueError('reverse must be a 2*1 list: [left_reverse, right_reverse]')

        self.left_motor.reverse(reverse[0])
        self.right_motor.reverse(reverse[1])


    def speed(self, speed=None):
        """
        Get or Set motors speed

        :param speed: [left_speed, right_speed] (-100.0~100.0)
        :type speed: [float/int, float/int]
        """
        if speed is None:
            return [self.left_motor.speed(), self.right_motor.speed()]

        if not isinstance(speed, list):
            raise ValueError('reverse must be a 2*1 list: [left_speed, right_speed]')
        elif len(speed) != 2:
            raise ValueError('reverse must be a 2*1 list: [left_speed, right_speed]')

        self.left_motor.speed(speed[0])
        self.right_motor.speed(speed[1])

    def forward(self, speed):
        """
        Forward

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed([speed, speed])

    def backward(self, speed):
        """
        Backward

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed([-speed, -speed])

    def turn_left(self, speed):
        """
        Left turn

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed([-speed, speed])

    def turn_right(self, speed):
        """
        Right turn

        :param speed: Motor speed(-100.0~100.0)
        :type speed: float
        """
        self.speed([speed, -speed])
