# Bella Hat

Bella Hat Python library for Raspberry Pi.

## Docs

<https://github.com/sunfounder/bella-hat/blob/main/docs/build/markdown/index.md>

## Installation

### Bella Hat Python library

Install dependencies:

```bash
sudo apt-get update
sudo apt-get install git python3-pip
```

Install in python venv:

```bash
git clone https://github.com/sunfounder/bella-hat.git
cd bella-hat
sudo pip3 install ./

```

if you need to install in system environment, you need add "--break-system-packages" parameter:

```bash
sudo pip3 install ./ --break-system-packages
```

Enable i2c and spi, need reboot to take effect:

```bash
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

Copy alsa config file:

```bash
sudo cp asound.conf /etc/asound.conf
```

> [!Warning]
See: <https://github.com/jgarff/rpi_ws281x>\
On an RPi 3 you have to change the GPU core frequency to 250 MHz, otherwise the SPI clock has the wrong frequency.\
Do this by adding the following line to /boot/firmware/config.txt and reboot:

```bash
core_freq=250
```

> [!Warning]
On an RPi 4 you must set a fixed frequency to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:\
Do this by adding the following lines to /boot/firmware/config.txt and reboot:

```bash
core_freq_min=500
```

### Factory Test

Install the factory test:

```bash
cd bella-factory-test
sudo bash install.sh
cd ..
```

### Bella AP helper

Install the Bella AP helper:

```bash
cd bella-ap
sudo bash install.sh
cd ..
```

## Create image

### Get image ready

1. Flash a Raspberry Pi OS Lite 64 bit on a microSD card.
2. Before flash, set up the information 
   1. hostname: bella
   2. username: pi
   3. password: raspberry
   4. SSH: enable
3. Insert the microSD card into the Raspberry Pi and power it on.
4. Wait for the Raspberry Pi to boot up and resize the partition.
5. shutdown and eject the microSD card.

### Shrink the image

Put the microSD card into another Raspberry Pi or other Linux computer. Find the device path of the microSD card:

'''bash
lsblk
```

i.e. 

```bash
/dev/sda
```

If it's mounted, unmount it: 

```bash
sudo umount /dev/sda1
sudo umount /dev/sda2
```

Checkout the start sector of the second partition:

```bash
sudo fdisk -l /dev/sda
```

```bash
Disk /dev/sda: 29.1 GiB, 31266439168 bytes, 61067264 sectors
Disk model: STORAGE DEVICE
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xab1a3c6b

Device     Boot   Start      End  Sectors  Size Id Type        
/dev/sda1          8192  1056767  1048576  512M  c W95 FAT32 (L
/dev/sda2       1056768 61067263 60010496 28.6G 83 Linux 
```

Note down `/dev/sda2` `Start` sector, here it's `1056768`.

Run e2fsck to check and repair the file system:

```bash
sudo e2fsck -f /dev/sda2
```

Shrink the file system to the minimum size:

```bash
sudo resize2fs -M /dev/sda2
```

Try multiple times until the file system is shrunk to the minimum size. like this:

```bash
The filesystem is already 854946 (4k) blocks long.  Nothing to do!
```

Note down the new block size of the file system, here it's `854946`.

```bash
sudo fdisk /dev/sda
```

1. Enter `p` to list the partitions.
2. Enter `d` to delete the second partition.
3. Enter `n` to create a new partition.
4. Enter `p` to select the partition type.
5. Enter `2` to select the second partition.
6. Enter the start sector of the second partition, which is `1056768`.
7. Calculate the size of the second partition with the above block size, `<block size> * 4` KB. here it's `854946 * 4 = 3440640` KB.
8. Enter the size of the second partition in format `+<size in KB>K`. here it's `+3440640K`.
9. Enter `n` to not remove the signature.
10. Enter `w` to write the changes and exit.

Run e2fsck to check and repair the file system again:

```bash
sudo e2fsck -f /dev/sda2
```

Now ecject the microSD card and put it back into the Raspberry Pi.

### Create the image

Boot up the microSD card. Checkout the new partition size:

```bash
df -h
```

It should look like this:

```bash
df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            1.6G     0  1.6G   0% /dev
tmpfs           380M  1.2M  379M   1% /run
/dev/mmcblk0p2  3.2G  2.2G  807M  74% /
tmpfs           1.9G     0  1.9G   0% /dev/shm
tmpfs           5.0M   20K  5.0M   1% /run/lock
/dev/mmcblk0p1  510M   64M  447M  13% /boot/firmware
tmpfs           380M     0  380M   0% /run/user/1000
```

Now do the [installation](#installation) above, reboot to take effect.

### Export the image

> [!Warning]
> Now you can't reboot the Raspberry Pi, or it will resize the partition again. And you will need to do above all ovver again. If you need to reboot, remove the `init` parameter from the `cmdline.txt` file. and add it back before exporting the image.

Power off and eject the microSD card and put it into another computer to export the image.

use Win32DiskImager on Windows.

1. Choose a image name like `bella-v0.0.1.img`.
2. Choose the microSD card device path, like [G:/].
3. Check Read Only Allocated Partitions.
4. Click Read.
5. Wait for the image to be created.

Now you can use this image to flash a new SD card and see if it works.

