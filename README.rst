Praline
#######

Praline is a Raspberry Pi based Bitcoin hardware wallet.

.. image:: https://raw.githubusercontent.com/zhouer/Praline/master/praline.jpg
    :alt: The Praline hardware wallet
    
Requirement
===========

You will need:

 * A `Respberry Pi Zero <https://www.raspberrypi.org/products/raspberry-pi-zero/>`_ or a `Raspberry Pi Zero W <https://www.raspberrypi.org/products/raspberry-pi-zero-w/>`_
  * Raspberry Pi 2/3 **DOES NOT** work because they cannot work in USB gadget mode.
 * An `Adafruit 128x64 OLED Bonnet for Raspberry Pi <https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/>`_ (optional)
  * You can go without the OLED and the buttons, and let this hardware wallet create and sign the transactions without confirmation.

Device-side installation
========================

The following steps should be done on the Raspberry Pi Zero.
Note: The Praline can work offline, but you will need internet access during the installation.

Run as an USB serial gadget
--------------------------

.. code-block:: sh

    sudo vi /boot/config.txt
    # Add "dtoverlay=dwc2" as the last line
    sudo vi /boot/cmdline.txt
    # Add "modules-load=dwc2,g_serial" after "rootwait"

Read `this <https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/serial-gadget>`_
for detail instructions, but stop after finish step 1, **DO NOT** enable logging in service on the serial port.

Enable I2C
----------

Install I2C utils

.. code-block:: sh

    sudo apt-get install i2c-tools python-smbus

and enable kernel support from the Raspberry Pi config tool

.. code-block:: sh

    sudo raspi-config
    # 5 Interfacing Options -> P5 I2C
    sudo reboot

Read `this <https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c>`_
for detail instructions. Note: the raspi-config interface was changed, see above.

Install Python scripts
----------------------

You can install Praline with pip

.. code-block:: sh

    sudo pip install praline

or install from source

.. code-block:: sh

    git clone https://github.com/zhouer/Praline
    cd Praline
    pip setup.py install

Run scripts at system boot
--------------------------

You can setup running the Python script at system boot by adding it into /etc/rc.local

.. code-block:: sh

    sudo vi /etc/rc.local
    # Add a line "/usr/local/bin/praline &" before "exit 0"

All done
--------

Now, you can un-plug all micro-USB cords, and plug one micro-USB cord back to the **USB (NOT PWR IN)** port.
It will take about 30 seconds to boot into Linux and run the Python script.

Host-side installation
======================

You will need a host-side application to talk with the Praline,
see instructions on `Praline-host <https://github.com/zhouer/Praline-host>`_
