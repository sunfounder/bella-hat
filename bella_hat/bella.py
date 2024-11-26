from .basic import _Basic_class
from .modules import Ultrasonic, DHT11, Grayscale_Module, LSM6DSOX
from .adc import ADC
from .pin import Pin
from .pwm import PWM
from .motor import Motors

class Bella(_Basic_class):
    LOW = False
    HIGH = True

    BAT_VOLT_ADC_CHANNEL = 4
    BAT_VOLT_GAIN = 3

    ULTRASONIC_TRING_PIN = 20
    ULTRASONIC_ECHO_PIN = 21

    DTH11_PIN = 19

    GARYSCALE_LEFT_ADC_CHANNEL = 2
    GARYSCALE_MIDDLE_ADC_CHANNEL = 1
    GARYSCALE_RIGHT_ADC_CHANNEL = 0

    LEFT_MOTOR_PWMA_CHANNEL = 18
    LEFT_MOTOR_PWMB_CHANNEL = 19
    RIGHT_MOTOR_PWMA_CHANNEL = 16
    RIGHT_MOTOR_PWMB_CHANNEL = 17

    BAT_MAX_VLOT = 8.4
    BAT_MIN_VLOT = 6.5

    FAN_PIN = 16
    FAN_ACTIVE = HIGH

    BTN_PIN = 25
    BTN_ACTIVE = LOW

    L_EYE_LED_PIN = 14
    R_EYE_LED_PIN = 15

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bat = ADC(self.BAT_VOLT_ADC_CHANNEL)
        self.ultrasonic = Ultrasonic(
                            trig=Pin(self.ULTRASONIC_TRING_PIN), 
                            echo=Pin(self.ULTRASONIC_ECHO_PIN, mode=Pin.IN, pull=Pin.PULL_DOWN)
                            )
        self.dht11 = DHT11(self.DTH11_PIN)
        self.grayscale = Grayscale_Module(
                            ADC(self.GARYSCALE_LEFT_ADC_CHANNEL),
                            ADC(self.GARYSCALE_MIDDLE_ADC_CHANNEL),
                            ADC(self.GARYSCALE_RIGHT_ADC_CHANNEL)
                            )
        self.motors = Motors(
                        self.LEFT_MOTOR_PWMA_CHANNEL,
                        self.LEFT_MOTOR_PWMB_CHANNEL, 
                        self.RIGHT_MOTOR_PWMA_CHANNEL,
                        self.RIGHT_MOTOR_PWMB_CHANNEL,
                        )
        self.lsm6dsox = LSM6DSOX()
        self.fan_state = False
        self.fan = Pin(self.FAN_PIN, mode=Pin.OUT)
        self.fan_off()
        self.btn = Pin(self.BTN_PIN, mode=Pin.IN)
        self.eye_l =  PWM(14)
        self.eye_r =  PWM(15)
        self.eye_l.freq(100)
        self.eye_r.freq(100)

    def get_battery_voltage(self):
        ''''
        Get the battery voltage.

        return: float - Battery voltage in volts.
        '''
        volt = round(self.bat.read_voltage()*self.BAT_VOLT_GAIN, 2)
        return volt

    def get_battery_percentage(self):
        '''
        Get the battery percentage.

        return: float - Battery percentage.
        '''
        vol = round(self.bat.read_voltage()*self.BAT_VOLT_GAIN, 2)
        perc = (vol - self.BAT_MIN_VLOT) / (self.BAT_MAX_VLOT - self.BAT_MIN_VLOT) * 100
        if perc > 100:
            perc = 100.0
        return round(perc, 1)
        
    def get_ultrasonic_distance(self):
        '''
        Get the distance from the ultrasonic sensor.

        return: float - Distance in cm.
                -1, timeout
                -2, distance limit exceeded
        '''
        return self.ultrasonic.read()

    def get_temperature(self): 
        '''
        Get the temperature from the DHT11 sensor.

        return: float - Temperature in Celsius.
        '''
        return self.dht11.temperature

    def get_humidity(self): 
        '''
        Get the humidity from the DHT11 sensor.
        
        return: float - Humidity in percentage.
        '''
        return self.dht11.humidity

    def get_grayscales(self):
        '''
        Get the grayscale sensor values.

        return: list - Grayscale sensor values.
        '''
        return self.grayscale.read()

    def set_motors(self, leftPercent, rightPercent):
        '''
        Set the motor percentage for left and right motors

        leftPercent: int - Motor percentage for left motor, -100 to 100
        rightPercent: int - Motor percentage for right motor, -100 to 100
        '''
        self.motors.speed([leftPercent, rightPercent])

    def set_motors_reverse(self, left_reverse, right_reverse):
        '''
        Set the motors is reversed or not

        left_reverse: bool - set left motor is reversed or not
        right_reverse: bool - set  right motor is reversed or not
        '''
        self.motors.speed([left_reverse, right_reverse])

    def get_acc(self):
        '''
        Get acceleration data of lsm6dsox sensor.
        
        return: list - [acc_x, acc_y, acc_z].
        '''
        return self.lsm6dsox.acc

    def get_gyro(self):
        '''
        Get gyro data of lsm6dsox sensor.
        
        return: list - [gyro_x, gyro_y, gyro_z].
        '''
        return self.lsm6dsox.gyro

    def fan_on(self):
        '''
        Open the fan on Bella HAT.
        '''
        self.fan_state = True
        self.fan.value(self.FAN_ACTIVE)
 

    def fan_off(self):
        '''
        Close the fan on Bella HAT.
        '''
        self.fan_state = False
        self.fan.value(not self.FAN_ACTIVE)

    def read_btn(self):
        '''
        Read the state of btn on Bella HAT.
        '''
        if self.BTN_ACTIVE:
            return self.btn.value()
        else:
            return not self.btn.value()

    def set_eyes_led(self, left_brightness, right_brightness):
        '''
        Set the front board LEDs brightness.

        left_brightness: int - brightness for left LEDs, 0 to 100
        right_brightness: int - brightness for right LEDs, 0 to 100
        '''
        if left_brightness > 100:
            left_brightness = 100
        elif left_brightness < 0:
            left_brightness = 0
        if right_brightness > 100:
            right_brightness = 100
        elif right_brightness < 0:
            right_brightness = 0
        self.eye_l.pulse_width_percent(left_brightness)
        self.eye_r.pulse_width_percent(right_brightness)

