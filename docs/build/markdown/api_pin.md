# class `Pin`

**Example**

Simple read or control pin:

```python
# Import Pin class
from robot_hat import Pin

# Create Pin object with numeric pin numbering and default input pullup enabled
d0 = Pin(16, Pin.IN, Pin.PULL_UP)
# Create Pin object with named pin numbering
d1 = Pin(25)

# read value
value0 = d0.value()
value1 = d1.value()
print(value0, value1)

# write value
d0.value(1) # force input to output
d1.value(0)

# set pin high/low
d0.high()
d1.off()
```

Interrupt:

```python
# Import Pin class
from bella_hat.pin import Pin

# set interrupt
led = Pin(16, Pin.OUT)
switch = Pin(25, Pin.IN, Pin.PULL_DOWN)
def onPressed(chn):
    led.value(not switch.value())
switch.irq(handler=onPressed, trigger=Pin.IRQ_RISING_FALLING)

while True:
    pass
```

**API**

### *class* bella_hat.pin.Pin(pin, mode=None, pull=None, \*args, \*\*kwargs)

Bases: [`_Basic_class`](api_basic_class.md#bella_hat.basic._Basic_class)

Pin manipulation class

#### OUT *= 1*

Pin mode output

#### IN *= 2*

Pin mode input

#### PULL_UP *= 17*

Pin internal pull up

#### PULL_DOWN *= 18*

Pin internal pull down

#### PULL_NONE *= None*

Pin internal pull none

#### IRQ_FALLING *= 33*

Pin interrupt falling

#### IRQ_RISING *= 34*

Pin interrupt falling

#### IRQ_RISING_FALLING *= 35*

Pin interrupt both rising and falling

#### \_\_init_\_(pin, mode=None, pull=None, \*args, \*\*kwargs)

Initialize a pin

* **Parameters:**
  * **pin** (*int/str*) – pin number of Raspberry Pi
  * **mode** (*int*) – pin mode(IN/OUT)
  * **pull** (*int*) – pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)

#### setup(mode, pull=None)

Setup the pin

* **Parameters:**
  * **mode** (*int*) – pin mode(IN/OUT)
  * **pull** (*int*) – pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)

#### dict(\_dict=None)

Set/get the pin dictionary

* **Parameters:**
  **\_dict** (*dict*) – pin dictionary, leave it empty to get the dictionary
* **Returns:**
  pin dictionary
* **Return type:**
  dict

#### \_\_call_\_(value)

Set/get the pin value

* **Parameters:**
  **value** (*int*) – pin value, leave it empty to get the value(0/1)
* **Returns:**
  pin value(0/1)
* **Return type:**
  int

#### value(value: bool = None)

Set/get the pin value

* **Parameters:**
  **value** (*int*) – pin value, leave it empty to get the value(0/1)
* **Returns:**
  pin value(0/1)
* **Return type:**
  int

#### on()

Set pin on(high)

* **Returns:**
  pin value(1)
* **Return type:**
  int

#### off()

Set pin off(low)

* **Returns:**
  pin value(0)
* **Return type:**
  int

#### high()

Set pin high(1)

* **Returns:**
  pin value(1)
* **Return type:**
  int

#### low()

Set pin low(0)

* **Returns:**
  pin value(0)
* **Return type:**
  int

#### irq(handler, trigger, bouncetime=200, pull=None)

Set the pin interrupt

* **Parameters:**
  * **handler** (*function*) – interrupt handler callback function
  * **trigger** (*int*) – interrupt trigger(RISING, FALLING, RISING_FALLING)
  * **bouncetime** (*int*) – interrupt bouncetime in miliseconds

#### name()

Get the pin name

* **Returns:**
  pin name
* **Return type:**
  str
