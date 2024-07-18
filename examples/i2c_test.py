from i2c import I2C
import time

I2C_ADDR = 0x16
i2c = I2C(I2C_ADDR)

while True:
    result = i2c.read_block_data(0, 19)
    print(result)
    time.sleep(1)