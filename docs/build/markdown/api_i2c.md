# class `I2C`

**Example**

```python
# Import the I2C class
from bella_hat.i2c import I2C

# You can scan for available I2C devices
print([f"0x{addr:02X}" for addr in I2C().scan()])
# You should see at least one device address 0x14, which is the
# on board MCU for PWM and ADC

# Initialize a I2C object with device address, for example
# to communicate with on board MCU 0x14
mcu = I2C(0x14)
# Send ADC channel register to read ADC, 0x10 is Channel 0, 0x11 is Channel 1, etc.
mcu.write([0x10, 0x00, 0x00])
# Read 2 byte for MSB and LSB
msb, lsb = mcu.read(2)
# Convert to integer
value = (msb << 8) + lsb
# Print the value
print(value)
```

For more information on the I2C protocol, see checkout adc.py and pwm.py

**API**

### *class* bella_hat.i2c.I2C(address=None, bus=1, \*args, \*\*kwargs)

Bases: [`_Basic_class`](api_basic_class.md#bella_hat.basic._Basic_class)

I2C bus read/write functions

#### \_\_init_\_(address=None, bus=1, \*args, \*\*kwargs)

Initialize the I2C bus

* **Parameters:**
  * **address** (*int*) – I2C device address
  * **bus** (*int*) – I2C bus number

#### *static* scan(busnum=1, force=False)

Scan the I2C bus for devices

* **Returns:**
  List of I2C addresses of devices found
* **Return type:**
  list

#### write(data)

Write data to the I2C device

* **Parameters:**
  **data** (*int/list/bytearray*) – Data to write
* **Raises:**
  ValueError if write is not an int, list or bytearray

#### read(length=1)

Read data from I2C device

* **Parameters:**
  **length** (*int*) – Number of bytes to receive
* **Returns:**
  Received data
* **Return type:**
  list

#### mem_write(data, memaddr)

Send data to specific register address

* **Parameters:**
  * **data** (*int/list/bytearray*) – Data to send, int, list or bytearray
  * **memaddr** (*int*) – Register address
* **Raises:**
  **ValueError** – If data is not int, list, or bytearray

#### mem_read(length, memaddr)

Read data from specific register address

* **Parameters:**
  * **length** (*int*) – Number of bytes to receive
  * **memaddr** (*int*) – Register address
* **Returns:**
  Received bytearray data or False if error
* **Return type:**
  list/False

#### is_avaliable()

Check if the I2C device is avaliable

* **Returns:**
  True if the I2C device is avaliable, False otherwise
* **Return type:**
  bool
