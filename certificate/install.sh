#!/bin/bash

set -e

sudo apt install -y bluez iw iperf3 rfkill bluez-hcidump screen

cd ~/bella-hat

rm -rf .venv
python3 -m venv .venv --system-site-packages
source .venv/bin/activate

# cd ~/bella-hat/vilib
# sudo python3 install.py 

cd ~/bella-hat
pip install ./




