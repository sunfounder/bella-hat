# class `_Basic_class`

`_Basic_class` is a logger class for all class to log, so if you want to see
logs of a class, just add a debug argument to it.

**Example**

```python
# See PWM log
from bella_hat.pwm import PWM

# init the class with a debug argument
pwm = PWM(0, debug_level="debug")

# run some functions and see logs
pwm.freq(1000)
pwm.pulse_width_percent(100)
```

**API**

### *class* bella_hat.basic.\_Basic_class(debug_level='warning')

Basic Class for all classes

with debug function

#### DEBUG_LEVELS *= {'critical': 50, 'debug': 10, 'error': 40, 'info': 20, 'warning': 30}*

Debug level

#### DEBUG_NAMES *= ['critical', 'error', 'warning', 'info', 'debug']*

Debug level names

#### \_\_init_\_(debug_level='warning')

Initialize the basic class

* **Parameters:**
  **debug_level** (*str/int*) – debug level, 0(critical), 1(error), 2(warning), 3(info) or 4(debug)

#### *property* debug_level

Debug level
