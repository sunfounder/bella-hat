Install
==========================================

#. Update your system.

  Make sure you are connected to the Internet and update your system:

  .. raw:: html
    <run></run>

  .. code-block::

      sudo apt update

  .. note::
      Python3 related packages must be installed if you are installing the **Lite** version OS.
      
      .. raw:: html
       <run></run>

      .. code-block::
      
       sudo apt install git python3-pip python3-setuptools python3-smbus
  
#. Download the source code.

  .. raw:: html

      <run></run>

  .. code-block::

     git clone https://github.com/sunfounder/bella-hat.git

#. Install

  It is recommended to install within a Python virtual environment.

  .. code-block::

      cd bella-hat
      pip3 install ./

  .. note::
      if you want to install in system environment. You need add parameter "--break-system-packages"
  
      .. code-block::

          pip3 install ./ --break-system-packages
