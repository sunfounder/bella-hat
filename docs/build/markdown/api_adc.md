# class `ADC`

**Example**

```python
# Import ADC class
from bella_hat.adc import ADC

# Create ADC object with numeric pin numbering
a0 = ADC(0)
# Create ADC object with named pin numbering
a1 = ADC('A1')

# Read ADC value
value0 = a0.read()
value1 = a1.read()
voltage0 = a0.read_voltage()
voltage1 = a1.read_voltage()
print(f"ADC 0 value: {value0}")
print(f"ADC 1 value: {value1}")
print(f"ADC 0 voltage: {voltage0}")
print(f"ADC 1 voltage: {voltage1}")
```

Read Battery voltage on Bella bella-hat:

> The battery voltage measurement terminal is connected to ADC channel 4 and divided by 3 times
```python
# Import ADC class
from bella_hat.adc import ADC

BAT_VOLT_GAIN = 3
bat = ADC('A4')

bat_value = bat.read()
bat_voltage = bat.read_voltage() * BAT_VOLT_GAIN
print(f"Battery adc value: {bat_value}, voltage: {bat_voltage:.2f} V")
```

**API**

### *class* bella_hat.adc.ADC(chn, address=None, \*args, \*\*kwargs)

Bases: [`I2C`](api_i2c.md#bella_hat.i2c.I2C)

Analog to digital converter

#### \_\_init_\_(chn, address=None, \*args, \*\*kwargs)

Analog to digital converter

* **Parameters:**
  **chn** (*int/str*) – channel number (0-7/A0-A7)

#### read()

Read the ADC value

* **Returns:**
  ADC value(0-4095)
* **Return type:**
  int

#### read_voltage()

Read the ADC value and convert to voltage

* **Returns:**
  Voltage value(0-3.3(V))
* **Return type:**
  float
