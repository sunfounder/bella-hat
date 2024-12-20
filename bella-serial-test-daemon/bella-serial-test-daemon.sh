#!/usr/bin/bash

BUTTON_PIN=25

if [ "$1" == "start" ]; then
    pinctrl set $BUTTON_PIN ip pu
    factoryMode=$(pinctrl get $BUTTON_PIN | awk '{print $5}')
    echo "Factory mode: $factoryMode"

    if [ "$factoryMode" == "lo" ]; then
        /usr/bin/python /opt/bella-serial-test-daemon/bella-serial-test-daemon.py &
    elif [ "$factoryMode" == "hi" ]; then
        echo "Button not pressed, exit factory mode"
        exit 0
    else
        echo "Button not pressed, exit"
        exit 0
    fi
elif [ "$1" == "stop" ]; then
    kill $(ps aux | grep bella-serial-test-daemon.py | awk '{print $2}')
elif [ "$1" == "log" ]; then
    tail -f /var/log/bella-serial-test-daemon.log
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
