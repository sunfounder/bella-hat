# bella-hat

Bella Hat Python library for Raspberry Pi.

## Docs

<https://github.com/sunfounder/bella-hat/blob/main/docs/build/markdown/index.md>

## Installation

### Bella Hat Python library

Install in python venv:

```bash
git clone https://github.com/sunfounder/bella-hat.git
cd bella-hat
sudo pip3 install ./

```

if you need to install in system environment, you need add "--break-system-packages" parameter:

```bash
sudo pip3 install ./ --break-system-packages
```

Enable i2c and spi

```bash
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

> [!Warning]
See: <https://github.com/jgarff/rpi_ws281x>\
On an RPi 3 you have to change the GPU core frequency to 250 MHz, otherwise the SPI clock has the wrong frequency.\
Do this by adding the following line to /boot/firmware/config.txt and reboot:

```bash
core_freq=250
```

> [!Warning]
On an RPi 4 you must set a fixed frequency to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:\
Do this by adding the following lines to /boot/firmware/config.txt and reboot:

```bash
core_freq_min=500
```

### Serial Test daemon

Install the serial test daemon:

```bash
cd bella-serial-test-daemon
sudo bash install.sh
```

### Bella AP helper

Install the Bella AP helper:

```bash
cd bella-ap
sudo bash install.sh
```
