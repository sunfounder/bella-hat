#!/bin/bash

# Check if user is root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 1
fi

echo "Installing Bella-AP..."
# Copy files to /usr/local/bin
cp bella-ap /usr/local/bin/
# Add execute permission to bella-ap
chmod +x /usr/local/bin/bella-ap
# Create a service for bella-ap
cp bella-ap.service /etc/systemd/system/
# Reload the systemd daemon
systemctl daemon-reload
# Enable the service
systemctl enable bella-ap.service
# Start the service
systemctl start bella-ap.service
echo "Bella-AP installed successfully!"
