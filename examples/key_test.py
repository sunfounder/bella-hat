import tty
import termios
import select
import sys
import time

settings = termios.tcgetattr(sys.stdin)

def getKey():
    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select.select([sys.stdin], [], [], 0.1) 
    if rlist:
        key = sys.stdin.read(1) 
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) 

    return key


while True:
    key = getKey().lower()
    if key != '':
        print(f'key: {key}')
    print(f'{time.time():.3f}')
    time.sleep(.1)
