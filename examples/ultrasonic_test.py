from bl100_hat.modules import Ultrasonic, Pin
from time import sleep


sonar = Ultrasonic(trig=Pin(20), echo=Pin(21))

while True:
    distance = sonar.read()
    print(f"Distance: {distance} cm")
    sleep(1)