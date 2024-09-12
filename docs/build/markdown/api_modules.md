# module `modules`

## class `Ultrasonic`

> **Example**

> ```python
> # Import Ultrasonic and Pin class
> from bella_hat.modules import Ultrasonic, Pin

> # Create Motor object
> us = Ultrasonic(Pin(20), Pin(21))

> # Read distance
> distance = us.read()
> print(f"Distance: {distance}cm")
> ```

> **API**

> ### *class* bella_hat.modules.Ultrasonic(trig, echo, timeout=0.02)

> #### \_\_init_\_(trig, echo, timeout=0.02)

> Initialize an ultrasonic distance sensor

> * **Parameters:**
>   * **trig** (*pin number*) – tring pin
>   * **echo** (*pin number*) – echo pin
>   * **timeout** (*float* *,* *seconds*) – set the timeout for detecting the return of sound waves

> #### read(times=10)

> Read the distance

> * **Parameters:**
>   **times** (*int*) – retry times
> * **Returns:**
>   - float, distance in centimeter
>   - 1, timeout or error

## class `Grayscale_Module`

> **Example**

> ```python
> # Import Grayscale_Module and ADC class
> from bella_hat.modules import Grayscale_Module, ADC

> # Create Grayscale_Module object, reference should be calculate from the value reads on white
> # and black ground, then take the middle as reference
> gs = Grayscale_Module(ADC(0), ADC(1), ADC(2), reference=[1000, 900, 1000])

> # Read Grayscale_Module datas
> datas = gs.read()
> print(f"Grayscale Module datas: {datas}")
> # or read a specific channel
> l = gs.read(gs.LEFT)
> m = gs.read(gs.MIDDLE)
> r = gs.read(gs.RIGHT)
> print(f"Grayscale Module left channel: {l}")
> print(f"Grayscale Module middle channel: {m}")
> print(f"Grayscale Module right channel: {r}")

> # Read Grayscale_Module simple states
> state = gs.read_status()
> print(f"Grayscale_Module state: {state}")
> ```

> **API**

> ### *class* bella_hat.modules.Grayscale_Module(pin0: [ADC](api_adc.md#bella_hat.adc.ADC), pin1: [ADC](api_adc.md#bella_hat.adc.ADC), pin2: [ADC](api_adc.md#bella_hat.adc.ADC), reference: int = None)

> 3 channel Grayscale Module

> #### LEFT *= 2*

> Left Channel

> #### MIDDLE *= 1*

> Middle Channel

> #### RIGHT *= 1*

> Right Channel

> #### \_\_init_\_(pin0: [ADC](api_adc.md#bella_hat.adc.ADC), pin1: [ADC](api_adc.md#bella_hat.adc.ADC), pin2: [ADC](api_adc.md#bella_hat.adc.ADC), reference: int = None)

> Initialize Grayscale Module

> * **Parameters:**
>   * **pin0** (*bella_hat.ADC/int*) – ADC object or int for channel 0
>   * **pin1** (*bella_hat.ADC/int*) – ADC object or int for channel 1
>   * **pin2** (*bella_hat.ADC/int*) – ADC object or int for channel 2
>   * **reference** (*1\*3 list* *,*  *[**int* *,* *int* *,* *int* *]*) – reference voltage

> #### reference(ref: list = None) → list

> Get Set reference value

> * **Parameters:**
>   **ref** (*list*) – reference value, None to get reference value
> * **Returns:**
>   reference value
> * **Return type:**
>   list

> #### read_status(datas: list = None) → list

> Read line status

> * **Parameters:**
>   **datas** (*list*) – list of grayscale datas, if None, read from sensor
> * **Returns:**
>   list of line status, 0 for white, 1 for black
> * **Return type:**
>   list

> #### read(channel: int = None) → list

> read a channel or all datas

> * **Parameters:**
>   **channel** (*int/None*) – channel to read, leave empty to read all. 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT
> * **Returns:**
>   list of grayscale data
> * **Return type:**
>   list

## class `DHT11`

> **Example**

> ```python
> # Import DHT11 class
> from bella_hat.modules import DHT11

> # Create DHT11 object
> dht11 = DHT11(19)

> # Read DHT11 datas
> temperature = dht11.temperature
> humidity = dht11.humidity
> print(f"Temperature: {temperature}'C, Humidity: {humidity}%")
> ```

> **API**

> ### *class* bella_hat.modules.DHT11(pin)

> #### \_\_init_\_(pin)

> Initialize DHT11 Module

> * **Parameters:**
>   **pin** (*pin number*) – DHT11 data pin

> #### *property* temperature

> Temperature

> #### *property* humidity

> Humidity

## class `LSM6DSOX`

> **Example**

> ```python
> # Import LSM6DSOX class
> from bella_hat.modules import LSM6DSOX

> # Create LSM6DSOX object
> lsm6dsox = LSM6DSOX()

> # Read LSM6DSOX datas
> acc = lsm6dsox.acc
> gyro = lsm6dsox.gyro
> print(f"acc: X:{acc[0]:.2f},    Y: {acc[1]:.2f},    Z: {acc[2]:.2f} m/s^2")
> print(f"gyro X:{gyro[0]:.2f},    Y: {gyro[1]:.2f},    Z: {gyro[2]:.2f} radians/s")
> ```

> **API**

> ### *class* bella_hat.modules.LSM6DSOX

> #### \_\_init_\_()

> Initialize LSM6DSOX Module

> #### *property* acc

> Acceleration

> #### *property* gyro

> Gyro
