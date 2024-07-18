from bl100_hat import PWM
from time import sleep

for i in range(0, 4, 1):
    _pwm = PWM(i)
    _pwm.freq(100)
    _pwm.pulse_width_percent(20)

for i in range(4, 8, 1):
    _pwm = PWM(i)
    _pwm.freq(200)
    _pwm.pulse_width_percent(40)
    sleep(.1)

for i in range(8, 12, 1):
    _pwm = PWM(i)
    _pwm.freq(300)
    _pwm.pulse_width_percent(50)
    sleep(.1)

for i in range(12, 16, 1):
    _pwm = PWM(i)
    _pwm.freq(400)
    _pwm.pulse_width_percent(60)
    sleep(.1)

for i in range(16, 20, 1):
    _pwm = PWM(i)
    _pwm.freq(500)
    _pwm.pulse_width_percent(80)
    sleep(.1)

while True:
    sleep(5)

