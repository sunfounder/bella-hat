# Bella Factory Test Daemon

A daemon for factory testing of Bella. It connects the software with serial communication.

## Install

```bash
sudo apt install python3-picamera2 --no-install-recommends
# sudo apt install python3-picamera2

sudo bash install.sh

# add auto web test mode flag
sudo touch /boot/firmware/bella-auto-web-test-mode
```

## Usage

1. Turn off the robot if it is on.
2. Hold the rear button, and turn on the robot.
3. Until you hear 'Factory Mode', release the rear button.
4. Now you can connect a USB cable to the robot and run the test software, or command it with a serial tool.

Or you can run the test software directly:
```bash
python3 bella-factory-test.py
```

## Serial Communication

- Baud rate: 460800

The test commands are sent through the serial port. Each sending needs to end with "\n".

### Commands
- `data_on`: # Enable sensor data streaming
- `data_off`: # Disable sensor data streaming
- `motor`: Test the motors, robot will move forward, backward, left, right and stop.
- `fan`: Test the fan, fan will turn on for 2 seconds, and turn off for 2 seconds.
- `record_play`: Record a voice for 3 seconds, and play the voice.
- `play`: Play music to test the speaker.
- `rgb_led`: Test the light ring, red, green, blue and white light rings, and stop.
- `camera`: Take a photo and return the base64 format image.
- `ap:<WIFI_CONFIG>`: Set the AP with Wi-Fi QR code format `WIFI:T:WPA;S:bella-876zyx;P:87654321;;`
- `white`: Calibrate the grayscale white.
- `black`: Calibrate the grayscale black.
- `aging`: turn on/off the motors and fan, and test the robot's aging.
- `auto_factory_mode`: Enable boot into factory mode.
- `sn:<SERIAL_NUMBER>`: Set the serial number.
