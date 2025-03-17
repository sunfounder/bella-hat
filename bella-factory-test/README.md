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
4. Now you can connect a USB cable to the robot and run the test software.

## Serial Communication

Commands are in Chinese characters.

### Commands

- `电机`: Test the motors, robot will move forward, backward, left, right and stop.
- `风扇`: Test the fan, fan will turn on for 2 seconds, and turn off for 2 seconds.
- `录播`: Record a voice for 3 seconds, and play the voice.
- `喇叭`: Play music to test the speaker.
- `灯`: Test the light ring, red, green, blue and white light rings, and stop.
- `相机`: Take a photo and return the base64 format image.
- `AP:WIFIXXX`: Set the AP with format `WIFI:T:WPA;S:bella-876zyx;P:87654321;;`
- `灰度白`: Calibrate the grayscale white.
- `灰度黑`: Calibrate the grayscale black.
- `老化`: turn on/off the motors and fan, and test the robot's aging.
