# Install

1. Update your system.

   Make sure you are connected to the Internet and update your system:
   ```default
   sudo apt update
   ```

   #### NOTE
   Python3 related packages must be installed if you are installing the **Lite** version OS.
   ```default
   sudo apt install git python3-pip python3-setuptools python3-smbus
   ```
2. Download the source code.
   ```default
   git clone https://github.com/sunfounder/bella-hat.git
   ```
3. Install the package.

   It is recommended to install within a Python virtual environment.
   ```default
   cd bella-hat
   pip3 install ./
   ```

   #### NOTE
   if you want to install in system environment. You need add parameter “–break-system-packages”
   ```default
   pip3 install ./ --break-system-packages
   ```
4. Enable i2c and spi
   ```default
   sudo raspi-config nonint do_i2c 0
   sudo raspi-config nonint do_spi 0
   ```

#### WARNING
See: <[https://github.com/jgarff/rpi_ws281x](https://github.com/jgarff/rpi_ws281x)>
<br/>
On an RPi 3 you have to change the GPU core frequency to 250 MHz, otherwise the SPI clock has the wrong frequency.
<br/>
Do this by adding the following line to “/boot/firmware/config.txt” and reboot:
<br/>
```default
core_freq=250
```

#### WARNING
On an RPi 4 you must set a fixed frequency to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:
<br/>
Do this by adding the following lines to /boot/firmware/config.txt and reboot:
<br/>
```default
core_freq_min=500
```
