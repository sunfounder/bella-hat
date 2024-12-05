Install
==========================================

#. Update your system.

   Make sure you are connected to the Internet and update your system:
 
   .. code-block::
 
       sudo apt update
 
   .. note::
       Python3 related packages must be installed if you are installing the **Lite** version OS.
       
       .. code-block::
       
          sudo apt install git python3-pip python3-setuptools python3-smbus


#. Download the source code.

   .. code-block::

      git clone https://github.com/sunfounder/bella-hat.git

#. Install the package.

   It is recommended to install within a Python virtual environment.

   .. code-block::

       cd bella-hat
       pip3 install ./

   .. note::
     if you want to install in system environment. You need add parameter "--break-system-packages"

     .. code-block::

         pip3 install ./ --break-system-packages

#. Enable i2c and spi

   .. code-block::

        sudo raspi-config nonint do_i2c 0
        sudo raspi-config nonint do_spi 0

.. warning::
    | See: <https://github.com/jgarff/rpi_ws281x>
    | On an RPi 3 you have to change the GPU core frequency to 250 MHz, otherwise the SPI clock has the wrong frequency.
    | Do this by adding the following line to "/boot/firmware/config.txt" and reboot:

    .. code-block::

        core_freq=250

.. warning::
    | On an RPi 4 you must set a fixed frequency to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:
    | Do this by adding the following lines to /boot/firmware/config.txt and reboot:

    .. code-block::

        core_freq_min=500
