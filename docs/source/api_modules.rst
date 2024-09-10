module ``modules``
==================================================

.. currentmodule:: bella_hat.modules.modules

class ``Ultrasonic``
-----------------------------------------

    **Example**

    .. code-block:: python

        # Import Ultrasonic and Pin class
        from bella_hat.modules import Ultrasonic, Pin

        # Create Motor object
        us = Ultrasonic(Pin("D2"), Pin("D3"))

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
        gs = Grayscale_Module(ADC(0), ADC(1), ADC(2), reference=2000)
        
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

    .. autoclass:: bella_hat.modules.Grayscale_Module
        :special-members: __init__
        :members:
