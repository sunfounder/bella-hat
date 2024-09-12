# class `PWM`

**Example**

```python
# Import PWM class
from bella_hat.pwm import PWM

# Create PWM object with numeric pin numbering and default input pullup enabled
p0 = PWM(0)
# Create PWM object with named pin numbering
p1 = PWM('P1')


# Set frequency will automatically set prescaller and period
# This is easy for device like Buzzer or LED, which you care
# about the frequency and pulse width percentage.
# this usually use with pulse_width_percent function.
# Set frequency to 1000Hz
p0.freq(1000)
print(f"Frequence: {p0.freq()} Hz")
print(f"Prescaler: {p0.prescaler()}")
print(f"Period: {p0.period()}")
# Set pulse width to 50%
p0.pulse_width_percent(50)

# Or set prescaller and period, will get a frequency from:
# frequency = PWM.CLOCK / prescaler / period
# With this setup you can tune the period as you wish.
# set prescaler to 64
p1.prescaler(64)
# set period to 4096 ticks
p1.period(4096)
print(f"Frequence: {p1.freq()} Hz")
print(f"Prescaler: {p1.prescaler()}")
print(f"Period: {p1.period()}")
# Set pulse width to 2048 which is also 50%
p1.pulse_width(2048)
```

**API**

### *class* bella_hat.pwm.PWM(channel, address=None, \*args, \*\*kwargs)

Bases: [`I2C`](api_i2c.md#bella_hat.i2c.I2C)

Pulse width modulation (PWM)

#### REG_CHN *= 32*

Channel register prefix

#### REG_PSC *= 64*

Prescaler register prefix

#### REG_ARR *= 68*

Period registor prefix

#### REG_PSC2 *= 80*

Prescaler register prefix

#### REG_ARR2 *= 84*

Period registor prefix

#### CLOCK *= 72000000.0*

Clock frequency

#### \_\_init_\_(channel, address=None, \*args, \*\*kwargs)

Initialize PWM

* **Parameters:**
  **channel** (*int/str*) – PWM channel number(0-13/P0-P13)

#### freq(freq=None)

Set/get frequency, leave blank to get frequency

* **Parameters:**
  **freq** (*float*) – frequency(0-65535)(Hz)
* **Returns:**
  frequency
* **Return type:**
  float

#### prescaler(prescaler=None)

Set/get prescaler, leave blank to get prescaler

* **Parameters:**
  **prescaler** (*int*) – prescaler(0-65535)
* **Returns:**
  prescaler
* **Return type:**
  int

#### period(arr=None)

Set/get period, leave blank to get period

* **Parameters:**
  **arr** (*int*) – period(0-65535)
* **Returns:**
  period
* **Return type:**
  int

#### pulse_width(pulse_width=None)

Set/get pulse width, leave blank to get pulse width

* **Parameters:**
  **pulse_width** (*float*) – pulse width(0-65535)
* **Returns:**
  pulse width
* **Return type:**
  float

#### pulse_width_percent(pulse_width_percent=None)

Set/get pulse width percentage, leave blank to get pulse width percentage

* **Parameters:**
  **pulse_width_percent** (*float*) – pulse width percentage(0-100)
* **Returns:**
  pulse width percentage
* **Return type:**
  float
