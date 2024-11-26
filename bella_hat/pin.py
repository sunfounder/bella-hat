#!/usr/bin/env python3
from .basic import _Basic_class
import RPi.GPIO as GPIO


class Pin(_Basic_class):
    """Pin manipulation class"""

    OUT = GPIO.OUT
    IN = GPIO.IN
    IRQ_FALLING = GPIO.FALLING
    IRQ_RISING = GPIO.RISING
    IRQ_RISING_FALLING = GPIO.BOTH
    PULL_UP = GPIO.PUD_UP
    PULL_DOWN = GPIO.PUD_DOWN
    PULL_NONE = None

    _dict = {
        "D0": 17,
        "D1": 4,  # Changed
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,  # Removed
        "D7": 4,  # Removed
        "D8": 5,  # Removed
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 25,  # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 5,  # Changed
        "CE": 8,
    }

    def __init__(self, pin, mode=None, pull=None, *args, **kwargs):
        """
        Initialize a pin

        :param pin: pin number of Raspberry Pi
        :type pin: int/str
        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        super().__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # parse pin
        if isinstance(pin, str):
            if pin not in self.dict().keys():
                raise ValueError(
                    f'Pin should be in {self._dict.keys()}, not "{pin}"')
            self._board_name = pin
            self._pin_num = self.dict()[pin]
        elif isinstance(pin, int):
            self._pin_num = pin
        else:
            raise ValueError(
                f'Pin should be in \'str\' or \'int\', not "{type(pin)}"')
        # setup
        self._value = 0
        self.setup(mode, pull)
        self._info("Pin init finished.")


    def setup(self, mode, pull=PULL_NONE):
        """
        Setup the pin

        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        # check mode
        if mode in [None, self.OUT, self.IN]:
            self._mode = mode
        else:
            raise ValueError(
                f'mode param error, should be None, Pin.OUT, Pin.IN')
        # check pull
        if pull in [self.PULL_NONE, self.PULL_DOWN, self.PULL_UP]:
            self._pull = pull
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )
        #
        if mode in [None, self.OUT]:
            GPIO.setup(self._pin_num, self.OUT)
        else:
            if pull != None:
                GPIO.setup(self._pin_num, self.IN, pull_up_down=pull)
            else:
                GPIO.setup(self._pin_num, self.IN)

    def dict(self, _dict=None):
        """
        Set/get the pin dictionary

        :param _dict: pin dictionary, leave it empty to get the dictionary
        :type _dict: dict
        :return: pin dictionary
        :rtype: dict
        """
        if _dict == None:
            return self._dict
        else:
            if not isinstance(_dict, dict):
                raise ValueError(
                    f'Argument should be a pin dictionary like {{"my pin": ezblock.Pin.cpu.GPIO17}}, not {_dict}'
                )
            self._dict = _dict

    def __call__(self, value):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        return self.value(value)

    def value(self, value: bool = None):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        if value == None:
            if self._mode in [None, self.OUT]:
                self.setup(self.IN)
            result = GPIO.input(self._pin_num)
            self._debug(f"read pin {self._pin_num}: {result}")
            return result
        else:
            if self._mode in [self.IN]:
                self.setup(self.OUT)
            if bool(value):
                value = 1
            GPIO.output(self._pin_num, value)
            return value

    def on(self):
        """
        Set pin on(high)

        :return: pin value(1)
        :rtype: int
        """
        return self.value(1)

    def off(self):
        """
        Set pin off(low)

        :return: pin value(0)
        :rtype: int
        """
        return self.value(0)

    def high(self):
        """
        Set pin high(1)

        :return: pin value(1)
        :rtype: int
        """
        return self.on()

    def low(self):
        """
        Set pin low(0)

        :return: pin value(0)
        :rtype: int
        """
        return self.off()

    def irq(self, handler, trigger, bouncetime=200, pull=None):
        """
        Set the pin interrupt

        :param handler: interrupt handler callback function
        :type handler: function
        :param trigger: interrupt trigger(RISING, FALLING, RISING_FALLING)
        :type trigger: int
        :param bouncetime: interrupt bouncetime in miliseconds
        :type bouncetime: int
        """
        # check trigger
        if trigger not in [
                self.IRQ_FALLING, self.IRQ_RISING, self.IRQ_RISING_FALLING
        ]:
            raise ValueError(
                f'trigger param error, should be None, Pin.IRQ_FALLING, Pin.IRQ_RISING, Pin.IRQ_RISING_FALLING'
            )

        # check pull
        if pull in [self.PULL_NONE, self.PULL_DOWN, self.PULL_UP]:
            self._pull = pull
            if pull == self.PULL_UP:
                _pull_up = True
            else:
                _pull_up = False
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )
        #
        GPIO.setup(self._pin_num, self.IN, self._pull)

        pressed_handler = None
        released_handler = None
        #
        GPIO.add_event_detect(self._pin_num, trigger, callback=handler, bouncetime=bouncetime)

    def name(self):
        """
        Get the pin name

        :return: pin name
        :rtype: str
        """
        return f"GPIO{self._pin_num}"
