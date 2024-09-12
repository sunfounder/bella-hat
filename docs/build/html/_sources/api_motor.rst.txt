module ``motor``
========================================

class ``Motors``
----------------------------------------

**Example**

Initilize

.. code-block:: python
    
    # Import Motor class
    from bella_hat.motor import Motors

    # Create Motor object
    motors = Motors()
    # Create Motor object with setting motors direction
    # motors = Motors(left_reversed=True, right_reversed=False)


Control motors power.

.. code-block:: python

    #
    motors.speed([50, 50])
    # stop
    motors.stop()

Setup motor direction.

.. code-block:: python

    # Go forward and see if both motor directions are correct
    motors.forward(100)
    # if you found a motor is running in the wrong direction
    # Use these function to correct it
    motors.reverse(True, True) # [left_reverse, right_reverse]
    # Run forward again and see if both motor directions are correct
    motors.forward(100)

Move functions

.. code-block:: python

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

**API**

.. currentmodule:: bella_hat.motor

.. autoclass:: Motors
    :show-inheritance:
    :special-members: __init__, __getitem__
    :members:

class ``Motor``
----------------------------------------

**Example**

.. code-block:: python
    
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

**API**

.. currentmodule:: bella_hat.motor

.. autoclass:: Motor
    :show-inheritance:
    :special-members: __init__
    :members:
