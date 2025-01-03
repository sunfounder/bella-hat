# Bella AP

A helper script to automatically host a access point for Bella.

SSID and password are stored in `/etc/bella-ap.conf`.

## Usage

```
# Read the configuration file and start the access point
sudo systemctl start bella-ap
# Stop the access point and start WiFi connection
sudo systemctl stop bella-ap
```

