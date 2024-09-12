# class `Bella`

The class `Bella` encapsulates the usage functions of all physical interfaces on the Bella HAT and presets the corresponding pin numbers.
For a more detailed example, you can refer to the [examples/basic_test.py](examples.md#basic-test) file.

**Example**

```python
from bella_hat.bella import Bella

bella = Bella()
bellas.et_motors_reverse(True, False)

bella.set_eyes_led(80, 80)
bella.set_motors(20, 20)
bella.fan_on()

batVolt = bella.get_battery_voltage()
batPerc = bella.get_battery_percentage()
distance = bella.get_ultrasonic_distance()
temp = bella.get_temperature()
hum = bella.get_humidity()
grayscale = bella.get_grayscales()
acc = bella.get_acc()
gyro = bella.get_gyro()
btn_state = bella.read_btn()
print(f'''
Battery:      {batPerc:.1f}  {batVolt:.2f} V
Ultrasonic:   {distance} cm
DHT11:        temperature: {temp}'C   humidity: {hum}%
LSM6DSOX:     acc: X:{acc[0]:.2f},    Y: {acc[1]:.2f},    Z: {acc[2]:.2f} m/s^2
              gyro X:{gyro[0]:.2f},    Y: {gyro[1]:.2f},    Z: {gyro[2]:.2f} radians/s
Grayscale:    {grayscale}
Fan:          {"on" if bella.fan_state else "off"}
Btn:          {"pressed" if btn_state else "released"}
''')
```

**API**

### *class* bella_hat.bella.Bella(\*args, \*\*kwargs)

Bases: [`_Basic_class`](api_basic_class.md#bella_hat.basic._Basic_class)

#### \_\_init_\_(\*args, \*\*kwargs)

Initialize the basic class

* **Parameters:**
  **debug_level** (*str/int*) – debug level, 0(critical), 1(error), 2(warning), 3(info) or 4(debug)

#### get_battery_voltage()

‘
Get the battery voltage.

return: float - Battery voltage in volts.

#### get_battery_percentage()

Get the battery percentage.

return: float - Battery percentage.

#### get_ultrasonic_distance()

Get the distance from the ultrasonic sensor.

return: float - Distance in cm.
: -1, timeout
  -2, distance limit exceeded

#### get_temperature()

Get the temperature from the DHT11 sensor.

return: float - Temperature in Celsius.

#### get_humidity()

Get the humidity from the DHT11 sensor.

return: float - Humidity in percentage.

#### get_grayscales()

Get the grayscale sensor values.

return: list - Grayscale sensor values.

#### set_motors(leftPercent, rightPercent)

Set the motor percentage for left and right motors

leftPercent: int - Motor percentage for left motor, -100 to 100
rightPercent: int - Motor percentage for right motor, -100 to 100

#### set_motors_reverse(left_reverse, right_reverse)

Set the motors is reversed or not

left_reverse: bool - set left motor is reversed or not
right_reverse: bool - set  right motor is reversed or not

#### get_acc()

Get acceleration data of lsm6dsox sensor.

return: list - [acc_x, acc_y, acc_z].

#### get_gyro()

Get gyro data of lsm6dsox sensor.

return: list - [gyro_x, gyro_y, gyro_z].

#### fan_on()

Open the fan on Bella HAT.

#### fan_off()

Close the fan on Bella HAT.

#### read_btn()

Read the state of btn on Bella HAT.

#### set_eyes_led(left_brightness, right_brightness)

Set the front board LEDs brightness.

left_brightness: int - brightness for left LEDs, 0 to 100
right_brightness: int - brightness for right LEDs, 0 to 100
