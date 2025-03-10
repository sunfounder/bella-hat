#!/usr/bin/bash

APP_FOLDER=/opt/bella-factory-test
FIRST_BOOT_FLAG=/boot/firmware/bella-firstboot
AUTO_FACTORY_MODE=/boot/firmware/bella-auto-factory-mode
APP_NAME=bella-factory-test

BUTTON_PIN=25

if [ "$1" == "start" ]; then
    pinctrl set $BUTTON_PIN ip pu
    factoryMode=$(pinctrl get $BUTTON_PIN | awk '{print $5}')
    echo "Factory mode: $factoryMode"

    if [ "$factoryMode" == "lo" ]; then
        /usr/bin/python $APP_FOLDER/$APP_NAME.py &
    # Check if FIRST_BOOT_FLAG exists
    elif [ -f $FIRST_BOOT_FLAG ]; then
        echo "First boot, expand file system"
        mv $FIRST_BOOT_FLAG $AUTO_FACTORY_MODE
        raspi-config nonint do_expand_rootfs
        reboot
    # Check if AUTO_FACTORY_MODE exists
    elif [ -f $AUTO_FACTORY_MODE ]; then
        echo "Auto factory mode, enter factory mode"
        # rm $AUTO_FACTORY_MODE
        /usr/bin/python $APP_FOLDER/$APP_NAME.py &
    elif [ "$factoryMode" == "hi" ]; then
        echo "Button not pressed, exit factory mode"
        exit 0
    else
        echo "Button not pressed, exit"
        exit 0
    fi
elif [ "$1" == "stop" ]; then
    kill $(ps aux | grep $APP_NAME.py | awk '{print $2}') || true
elif [ "$1" == "log" ]; then
    tail -f /var/log/$APP_NAME.log
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
