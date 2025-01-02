#!/bin/bash

echo "Uninstalling Bella-AP..."

# Remove the service
sudo systemctl stop bella-ap.service
sudo systemctl disable bella-ap.service
sudo rm /etc/systemd/system/bella-ap.service

# Remove the executable
sudo rm /usr/local/bin/bella-ap

# Remove the configuration file
sudo rm /etc/bella-ap.conf

echo "Bella-AP has been uninstalled."
