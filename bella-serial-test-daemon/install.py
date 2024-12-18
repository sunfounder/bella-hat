# This script is to install a test daemon for bella.

import os
import subprocess

need_reboot = False

# Check root permission
if os.geteuid()!= 0:
    print("This script must be run as root")
    exit(1)

folder_name = "bella-serial-test-daemon"


# Check if serial hardware is enabled
result = subprocess.check_output("raspi-config nonint get_serial_hw", shell=True)
if result == 1:
    # Enable serial hardware
    os.system("raspi-config nonint do_serial_hw 0")
    need_reboot = True

# Check if serial console is disabled
result = subprocess.check_output("raspi-config nonint get_serial_cons", shell=True)
if result == 0:
    # Disable serial console
    os.system("raspi-config nonint do_serial_cons 1")
    need_reboot = True

# See if we need to reboot
if need_reboot:
    while True:
        # Prompt user to reboot
        result = input("Do you want to reboot now to apply the changes? (y/n) ")
        result = result.strip().lower()
        if result == "y":
            os.system("sudo reboot")
        elif result == "n":
            print("Cancled")
            exit(0)
        else:
            print("Invalid input. Rebooting later is recommended.")


# Copy folder to /opt
print(f"Copying script to /opt")
if os.path.exists(f"/opt/{folder_name}"):
    os.system(f"rm -rf /opt/{folder_name}")
os.system(f"cp -r ../{folder_name} /opt/{folder_name}")
# Copy executable to /usr/local/bin
print("Copying executable to /usr/local/bin")
os.system("cp bella-serial-test-daemon.sh /usr/local/bin/bella-serial-test-daemon")
# Set executable permission
os.system("chmod +x /usr/local/bin/bella-serial-test-daemon")
# Copy service to /etc/systemd/system
print("Copying service to /etc/systemd/system")
os.system("cp bella-serial-test-daemon.service /etc/systemd/system/bella-serial-test-daemon.service")
# Enable service
print("Enabling service")
os.system("systemctl enable bella-serial-test-daemon.service")
# Start service
print("Starting service")
os.system("systemctl restart bella-serial-test-daemon.service")
