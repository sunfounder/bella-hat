#!/bin/bash

APP_NAME="bella-factory-test"

echo "Uninstalling Bella Hat Factory Test..."
echo "Removing service..."
systemctl stop $APP_NAME.service
systemctl disable $APP_NAME.service
rm /etc/systemd/system/$APP_NAME.service

echo "Removing executable..."
rm /usr/local/bin/$APP_NAME

echo "Removing files..."
rm -rf /var/log/$APP_NAME.log
rm -rf /opt/$APP_NAME

read -p "Do you want to change Serial back to system default? (Disable Serial port, and enable Serial console) (y/n) " result
if [ "$result" = "y" ]; then
    raspi-config nonint do_serial_hw 1
    raspi-config nonint do_serial_cons 0
fi

echo "Done, now serial port is disabled and serial console is enabled. You can also change it under raspi-config."
echo "Uninstallation complete."
