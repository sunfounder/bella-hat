from bl100_hat.modules import DHT11
from time import sleep

# sudo python3 -m pip install adafruit-circuitpython-dht --break-system-packages
# sudo apt install python3-rpi-lgpio

dht11 = DHT11(19)

while True:
    temp = dht11.temperature
    humidity = dht11.humidity
    print(f"Temperature: {temp} 'C, humidity: {humidity}")

    sleep(1)