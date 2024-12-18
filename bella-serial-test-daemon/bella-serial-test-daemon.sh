#!/usr/bin/bash

if [ "$1" == "start" ]; then
    /usr/bin/python /opt/bella-serial-test-daemon/bella-serial-test-daemon.py debug &
elif [ "$1" == "stop" ]; then
    kill $(ps aux | grep bella-serial-test-daemon.py | awk '{print $2}')
elif [ "$1" == "log" ]; then
    tail -f /var/log/bella-serial-test-daemon.log
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
