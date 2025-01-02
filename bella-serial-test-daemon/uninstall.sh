#!/bin/bash

echo "Uninstalling Bella Hat Serial Test Daemon..."
echo "Removing service..."
systemctl stop bella-serial-test-daemon.service
systemctl disable bella-serial-test-daemon.service
rm /etc/systemd/system/bella-serial-test-daemon.service

echo "Removing executable..."
rm /usr/local/bin/bella-serial-test-daemon

echo "Removing files..."
rm -rf /var/log/bella-serial-test-daemon.log
rm -rf /opt/bella-serial-test-daemon

read -p "Do you want to change Serial back to system default? (Disable Serial port, and enable Serial console) (y/n) " result
if [ "$result" = "y" ]; then
    raspi-config nonint do_serial_hw 1
    raspi-config nonint do_serial_cons 0
fi

echo "Done, now serial port is disabled and serial console is enabled. You can also change it under raspi-config."
echo "Uninstallation complete."
