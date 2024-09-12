# Install

1. Update your system.

   Make sure you are connected to the Internet and update your system:
   ```default
   sudo apt update
   ```

   #### NOTE
   Python3 related packages must be installed if you are installing the **Lite** version OS.
   ```default
   sudo apt install git python3-pip python3-setuptools python3-smbus
   ```
2. Download the source code.
   ```default
   git clone https://github.com/sunfounder/bella-hat.git
   ```
3. Install the package.

   It is recommended to install within a Python virtual environment.
   ```default
   cd bella-hat
   pip3 install ./
   ```

   #### NOTE
   if you want to install in system environment. You need add parameter “–break-system-packages”
   ```default
   pip3 install ./ --break-system-packages
   ```
