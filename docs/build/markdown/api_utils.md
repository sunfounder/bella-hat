# module `utils`

### bella_hat.utils.set_volume(value)

Set volume

* **Parameters:**
  **value** (*int*) – volume(0~100)

### bella_hat.utils.run_command(cmd)

Run command and return status and output

* **Parameters:**
  **cmd** (*str*) – command to run
* **Returns:**
  status, output
* **Return type:**
  tuple

### bella_hat.utils.is_installed(cmd)

Check if command is installed

* **Parameters:**
  **cmd** (*str*) – command to check
* **Returns:**
  True if installed
* **Return type:**
  bool

### bella_hat.utils.mapping(x, in_min, in_max, out_min, out_max)

Map value from one range to another range

* **Parameters:**
  * **x** (*float/int*) – value to map
  * **in_min** (*float/int*) – input minimum
  * **in_max** (*float/int*) – input maximum
  * **out_min** (*float/int*) – output minimum
  * **out_max** (*float/int*) – output maximum
* **Returns:**
  mapped value
* **Return type:**
  float/int

### bella_hat.utils.get_ip(ifaces=['wlan0', 'eth0'])

Get IP address

* **Parameters:**
  **ifaces** (*list*) – interfaces to check
* **Returns:**
  IP address or False if not found
* **Return type:**
  str/False

### bella_hat.utils.reset_mcu()

Reset mcu on BL100 Hat.

This is helpful if the mcu somehow stuck in a I2C data
transfer loop, and Raspberry Pi getting IOError while
Reading ADC, manipulating PWM, etc.

### bella_hat.utils.get_battery_voltage()

Get battery voltage

* **Returns:**
  battery voltage(V)
* **Return type:**
  float
