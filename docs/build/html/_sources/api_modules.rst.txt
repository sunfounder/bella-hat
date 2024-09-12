module ``modules``
==================================================

.. currentmodule:: bella_hat.modules

class ``Ultrasonic``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Ultrasonic and Pin class
        from bella_hat.modules import Ultrasonic, Pin

        # Create Motor object
        us = Ultrasonic(Pin(20), Pin(21))

        # Read distance
        distance = us.read()
        print(f"Distance: {distance}cm")

    **API**

    .. autoclass:: Ultrasonic
        :special-members: __init__
        :members:


class ``Grayscale_Module``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Grayscale_Module and ADC class
        from bella_hat.modules import Grayscale_Module, ADC
        
        # Create Grayscale_Module object, reference should be calculate from the value reads on white
        # and black ground, then take the middle as reference
        gs = Grayscale_Module(ADC(0), ADC(1), ADC(2), reference=[1000, 900, 1000])
        
        # Read Grayscale_Module datas
        datas = gs.read()
        print(f"Grayscale Module datas: {datas}")
        # or read a specific channel
        l = gs.read(gs.LEFT)
        m = gs.read(gs.MIDDLE)
        r = gs.read(gs.RIGHT)
        print(f"Grayscale Module left channel: {l}")
        print(f"Grayscale Module middle channel: {m}")
        print(f"Grayscale Module right channel: {r}")

        # Read Grayscale_Module simple states
        state = gs.read_status()
        print(f"Grayscale_Module state: {state}")

    **API**

    .. autoclass:: Grayscale_Module
        :special-members: __init__
        :members:

class ``DHT11``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import DHT11 class
        from bella_hat.modules import DHT11
        
        # Create DHT11 object
        dht11 = DHT11(19)

        # Read DHT11 datas
        temperature = dht11.temperature
        humidity = dht11.humidity
        print(f"Temperature: {temperature}'C, Humidity: {humidity}%")

    **API**

    .. autoclass:: DHT11
        :special-members: __init__
        :members:

class ``LSM6DSOX``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import LSM6DSOX class
        from bella_hat.modules import LSM6DSOX
        
        # Create LSM6DSOX object
        lsm6dsox = LSM6DSOX()

        # Read LSM6DSOX datas
        acc = lsm6dsox.acc
        gyro = lsm6dsox.gyro
        print(f"acc: X:{acc[0]:.2f},    Y: {acc[1]:.2f},    Z: {acc[2]:.2f} m/s^2")
        print(f"gyro X:{gyro[0]:.2f},    Y: {gyro[1]:.2f},    Z: {gyro[2]:.2f} radians/s")

    **API**

    .. autoclass:: LSM6DSOX
        :special-members: __init__
        :members:
