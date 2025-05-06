#!/bin/bash

# Check if the script is run with sudo
if [[ $EUID -ne 0 ]]; then
    echo "ERROR: This script must be run as root (use sudo)." >&2
    exit 1
fi

# Get the speaker volume from command line parameter or use 70% as default
SPEAKER_VOLUME="${1:-70%}"
echo "Script is running with sudo privileges. Using speaker volume: $SPEAKER_VOLUME"

read_audioconf() {
    result=$(aplay -l | grep -A1 "USB Audio Device")
    card_number=$(echo "$result" | grep -oP 'card \K\d+')
    device_number=$(echo "$result" | grep -oP 'device \K\d+')

    if [[ -n "$card_number" && -n "$device_number" ]]; then
        echo "setting to hw:$card_number,$device_number ..."
        export SDL_AUDIODRIVER=alsa
        export AUDIODEV="hw:$card_number,$device_number"    
    else
        echo "ERROR: USB Audio Device not found" >&2
        exit 1
    fi
}

update_asound_conf() {
    # Call read_audioconf to get card_number and device_number
    result=$(aplay -l | grep -A1 "USB Audio Device")
    card_number=$(echo "$result" | grep -oP 'card \K\d+')
    device_number=$(echo "$result" | grep -oP 'device \K\d+')

    if [[ -n "$card_number" && -n "$device_number" ]]; then
        echo "Setting /etc/asound.conf with hw:$card_number,$device_number"
        
        cat <<EOF | sudo tee /etc/asound.conf > /dev/null
pcm.!default {
    type plug
    slave {
        pcm "plughw:$card_number,$device_number"
    }
}

ctl.!default {
    type hw
    card $card_number
}
EOF

        echo "/etc/asound.conf has been updated with card number $card_number and device number $device_number"
    else
        echo "ERROR: USB Audio Device not found. /etc/asound.conf was not updated." >&2
        exit 1  # Exit if the device is not found
    fi
}

increase_volume() {
    # Get the card number of the USB Audio Device
    USB_CARD=$(aplay -l | grep "USB Audio Device" | awk -F ':' '{print $1}' | sed 's/card //')

    # Check if the USB Audio Device card number is found
    if [ -n "$USB_CARD" ]; then
        # Set the volume of the USB Audio Device based on the provided parameter
        amixer -c "$USB_CARD" sset 'Speaker',0 "$SPEAKER_VOLUME"
        # Check if the volume was successfully set
        if [ $? -eq 0 ]; then
            echo "USB Audio Device (card $USB_CARD) volume set to $SPEAKER_VOLUME."
        else
            echo "Failed to set USB Audio Device (card $USB_CARD) volume."
        fi
    else
        echo "USB Audio Device not found."
    fi    
}

read_audioconf
update_asound_conf
increase_volume
