
import os

print("Uninstalling Bella Hat Serial Test Daemon...")
print("Removing service...")
os.system("systemctl stop bella-serial-test-daemon.service")
os.system("systemctl disable bella-serial-test-daemon.service")
os.system("rm /etc/systemd/system/bella-serial-test-daemon.service")
print("Removing executable...")
os.system("rm /usr/local/bin/bella-serial-test-daemon")
print("Removing files...")
os.system("rm -rf /var/log/bella-serial-test-daemon.log")
os.system("rm -rf /opt/bella-serial-test-daemon")

input("Do you want to change Serial back to system default? (Disable Serial port, and enable Serial console) (y/n) ")
if input == "y":
    os.system("raspi-config nonint do_serial_hw 1")
    os.system("raspi-config nonint do_serial_cons 0")
print("Done, now serial port is disabled and serial console is enabled. you can also change it under raspi-config.")

print("Uninstallation complete.")
