# module `motor`

## class `Motors`

**Example**

Initilize

```python
# Import Motor class
from bella_hat.motor import Motors

# Create Motor object
motors = Motors()
# Create Motor object with setting motors direction
# motors = Motors(left_reversed=True, right_reversed=False)
```

Control motors power.

```python
#
motors.speed([50, 50])
# stop
motors.stop()
```

Setup motor direction.

```python
# Go forward and see if both motor directions are correct
motors.forward(100)
# if you found a motor is running in the wrong direction
# Use these function to correct it
motors.reverse(True, True) # [left_reverse, right_reverse]
# Run forward again and see if both motor directions are correct
motors.forward(100)
```

Move functions

```python
import time

motors.forward(100)
time.sleep(1)
motors.backward(100)
time.sleep(1)
motors.turn_left(100)
time.sleep(1)
motors.turn_right(100)
time.sleep(1)
motors.stop()
```

**API**

### *class* bella_hat.motor.Motors(left_motor_pwma=18, left_motor_pwmb=19, right_motor_pwma=16, right_motor_pwmb=17, left_reversed=False, right_reversed=False, \*args, \*\*kwargs)

Bases: [`_Basic_class`](api_basic_class.md#bella_hat.basic._Basic_class)

#### \_\_init_\_(left_motor_pwma=18, left_motor_pwmb=19, right_motor_pwma=16, right_motor_pwmb=17, left_reversed=False, right_reversed=False, \*args, \*\*kwargs)

Initialize motors with bella_hat.motor.Motor

* **Parameters:**
  * **left_motor_pwma** (*int* *,* *pin number*) – pwma input for left motor
  * **left_motor_pwmb** (*int* *,* *pin number*) – pwmb input for left motor
  * **right_motor_pwma** (*int* *,* *pin number*) – pwma input for right motor
  * **right_motor_pwmb** (*int* *,* *pin number*) – pwmb input for right motor
  * **left_reversed** (*bool*) – whether to reverse left motor
  * **right_reversed** (*bool*) – whether to reverse right motor

#### stop()

Stop all motors

#### brake()

Brake

#### reverse(reverse=None)

Get or set motors is reversed or not

* **Parameters:**
  **reverse** ( *[**bool* *,* *bool* *]*) – [left_reverse, right_reverse]

#### speed(speed=None)

Get or Set motors speed

* **Parameters:**
  **speed** ( *[**float/int* *,* *float/int* *]*) – [left_speed, right_speed] (-100.0~100.0)

#### forward(speed)

Forward

* **Parameters:**
  **speed** (*float*) – Motor speed(-100.0~100.0)

#### backward(speed)

Backward

* **Parameters:**
  **speed** (*float*) – Motor speed(-100.0~100.0)

#### turn_left(speed)

Left turn

* **Parameters:**
  **speed** (*float*) – Motor speed(-100.0~100.0)

#### turn_right(speed)

Right turn

* **Parameters:**
  **speed** (*float*) – Motor speed(-100.0~100.0)

## class `Motor`

**Example**

```python
# Import Motor class
from bella_hat.motor import Motor, PWM, Pin

# Create Motor object
motor = Motor(18, 19) # pwma, pwmb

# Motor clockwise at 100% speed
motor.speed(100)
# Motor counter-clockwise at 100% speed
motor.speed(-100)

# If you like to reverse the motor direction
motor.reverse(True)
```

**API**

### *class* bella_hat.motor.Motor(pwma, pwmb, reversed=False)

Bases: `object`

#### \_\_init_\_(pwma, pwmb, reversed=False)

Initialize a motor

* **Parameters:**
  * **pwma** (*pin number*) – Motor speed control pwm input A pin
  * **pwmb** (*pin number*) – Motor speed control pwm input B pin
* **Reversed:**
  Whether to reverse the direction of motor rotation

#### speed(speed=None)

Get or set motor speed

* **Parameters:**
  **speed** (*int* *or* *float*) – Motor speed(-100.0~100.0)

#### reverse(reverse=None)

Get or set motor is reversed or not

* **Parameters:**
  **reverse** (*bool*) – True or False

#### brake()

#### stop()
