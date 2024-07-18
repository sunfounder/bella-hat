from bl100_hat import ADC
from time import sleep

a0 = ADC(0)
a1 = ADC(1)
a2 = ADC(2)
a3 = ADC(3)
a4 = ADC(4)

while True:
    a0_val = a0.read()
    a0_vol = a0.read_voltage()
    a1_val = a1.read()
    a1_vol = a1.read_voltage()
    a2_val = a2.read()
    a2_vol = a2.read_voltage()
    a3_val = a3.read()
    a3_vol = a3.read_voltage()
    a4_val = a4.read()
    a4_vol = a4.read_voltage()

    print(f"a0: {a0_val}, {a0_vol:.3f}")
    print(f"a1: {a1_val}, {a1_vol:.3f}")
    print(f"a2: {a2_val}, {a2_vol:.3f}")
    print(f"a3: {a3_val}, {a3_vol:.3f}")
    print(f"a4: {a4_val}, {a4_vol:.3f}, {a4_vol*3:.3f}")
    print()

    sleep(1)
