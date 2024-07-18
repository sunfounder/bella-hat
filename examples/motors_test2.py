from bl100_hat.motor import Motor, Motors
from time import sleep


def test_motor():
    lm = Motor(18, 19, False)
    rm = Motor(16, 17, False)

    try:
        while True:
            lm.brake()
            rm.brake()
            sleep(.1)

            for i in range(10, 101, 10):
                lm.speed(i)
                rm.speed(i)
                print(f'reverse: {[lm.reverse(), rm.reverse()]}, speed: {[lm.speed(), rm.speed()]}')
                sleep(.5)
            print()

            lm.brake()
            rm.brake()
            sleep(.1)


            lm.reverse(True)
            rm.reverse(True)
            for i in range(10, 101, 10):
                lm.speed(i)
                rm.speed(i)
                print(f'reverse: {[lm.reverse(), rm.reverse()]}, speed: {[lm.speed(), rm.speed()]}')
                sleep(.5)
            print()

            lm.brake()
            rm.brake()

            for i in range(10, -101, -10):
                lm.speed(i)
                rm.speed(i)
                print(f'reverse: {[lm.reverse(), rm.reverse()]}, speed: {[lm.speed(), rm.speed()]}')
                sleep(.5)
            print()


    finally:
        print('stop')
        lm.stop()
        rm.stop()


def test_motors():
    # car = Motors()
    car = Motors(18, 19, 16, 17, False, False)

    try:
        while True:
            # car.brake()
            # sleep(.1)

            # for i in range(10, 101, 10):
            #     car.speed([i, i])
            #     print(f'reverse: {car.reverse()}, speed: {car.speed()}')
            #     sleep(.5)
            # print()

            # car.brake()
            # sleep(.1)

            car.reverse([True, True])


            # for i in range(10, 101, 10):
            #     car.speed([i, i])
            #     print(f'reverse: {car.reverse()}, speed: {car.speed()}')
            #     sleep(.5)
            # print()

            # car.brake()
            # sleep(.1)

            # for i in range(-10, -101, -10):
            #     car.speed([i, i])
            #     print(f'reverse: {car.reverse()}, speed: {car.speed()}')
            #     sleep(.5)
            # print()

            # car.brake()
            # sleep(.1)

            # for i in range(10, 101, 10):
            #     car.forward(i)
            #     print(f'reverse: {car.reverse()}, speed: {car.speed()}')
            #     sleep(.5)
            # print()

            # car.brake()
            # sleep(.1)

            # for i in range(10, 101, 10):
            #     car.backward(i)
            #     print(f'reverse: {car.reverse()}, speed: {car.speed()}')
            #     sleep(.5)
            # print()

            car.brake()
            sleep(.1)

            for i in range(10, 101, 10):
                car.turn_left(i)
                print(f'reverse: {car.reverse()}, speed: {car.speed()}')
                sleep(.5)
            print()

            car.brake()
            sleep(.1)
    finally:
        print('stop')
        car.stop()

if __name__ == '__main__':
    # test_motor()
    test_motors()


