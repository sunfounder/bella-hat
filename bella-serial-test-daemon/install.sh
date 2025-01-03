#!/bin/bash

# This script is to install a test daemon for bella.

need_reboot=false

# Check root permission
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

folder_name="bella-serial-test-daemon"

echo "Checking if serial console is enabled"
result=$(raspi-config nonint get_serial_cons)
if [ "$result" -eq 0 ]; then
    # Disable serial console
    raspi-config nonint do_serial_cons 1
    echo "Serial console is enabled. Disabling it now."
    need_reboot=true
else
    echo "Serial console is already disabled."
fi

echo "Checking if serial hardware is enabled"
# Check if serial hardware is enabled
result=$(raspi-config nonint get_serial_hw)
if [ "$result" -eq 1 ]; then
    # Enable serial hardware
    raspi-config nonint do_serial_hw 0
    echo "Serial hardware is disabled. Enabling it now."
    need_reboot=true
else
    echo "Serial hardware is already enabled."
fi

# Copy folder to /opt
echo "Copying script to /opt"
if [ -d "/opt/$folder_name" ]; then
    rm -rf "/opt/$folder_name"
fi
cp -r "../$folder_name" "/opt/$folder_name"

# Copy executable to /usr/local/bin
echo "Copying executable to /usr/local/bin"
cp "bella-serial-test-daemon.sh" "/usr/local/bin/bella-serial-test-daemon"

# Set executable permission
chmod +x "/usr/local/bin/bella-serial-test-daemon"

# Copy service to /etc/systemd/system
echo "Copying service to /etc/systemd/system"
cp "bella-serial-test-daemon.service" "/etc/systemd/system/bella-serial-test-daemon.service"

# Reload systemd
systemctl daemon-reload

# Enable service
echo "Enabling service"
systemctl enable bella-serial-test-daemon.service

# Start service
echo "Starting service"
systemctl restart bella-serial-test-daemon.service

# See if we need to reboot
if [ "$need_reboot" = true ]; then
    while true; do
        # Prompt user to reboot
        read -p "Do you want to reboot now to apply the changes? (y/n) " result
        result=$(echo "$result" | tr '[:upper:]' '[:lower:]')
        if [ "$result" = "y" ]; then
            reboot
        elif [ "$result" = "n" ]; then
            echo "Canceled"
            exit 0
        else
            echo "Invalid input. Rebooting later is recommended."
        fi
    done
fi
