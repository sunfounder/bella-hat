from bl100_hat import PWM
from time import sleep

a_in = PWM(16)
b_in = PWM(17)

a2_in = PWM(18)
b2_in = PWM(19)

a_in.freq(100)
b_in.freq(100)
a2_in.freq(100)
b2_in.freq(100)


def forward(power):
    a_in.pulse_width_percent(power)
    b_in.pulse_width_percent(0)
    a2_in.pulse_width_percent(power)
    b2_in.pulse_width_percent(0)
    
def backward(power):
    a_in.pulse_width_percent(0)
    b_in.pulse_width_percent(power)

def stop():
    a_in.pulse_width_percent(0)
    b_in.pulse_width_percent(0)
    a2_in.pulse_width_percent(0)
    b2_in.pulse_width_percent(0)

def brake():
    a_in.pulse_width_percent(100)
    b_in.pulse_width_percent(100)


try:
    while True:

        # for i in range(0, 101, 10):
        #     a_in.freq(200)
        #     b_in.freq(200)
        #     backward(i)
        #     sleep(.5)
        # sleep(.5)

        # brake()
        # sleep(.1)

        # for i in range(0, 101, 10):
        #     a_in.freq(200)
        #     b_in.freq(200)
        #     forward(i)
        #     sleep(.5)
        # sleep(.5)

        # brake()
        # sleep(.1)


        a_in.freq(200)
        b_in.freq(200)
        forward(90)
        sleep(1)
        # backward(100)
        # sleep(1)
finally:
    print('stop')
    stop()
    sleep(.1)




