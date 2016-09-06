pyXL320
=========

.. image:: https://landscape.io/github/walchko/pyxl320/master/landscape.svg?style=flat
   :target: https://landscape.io/github/walchko/pyxl320/master
   :alt: Code Health
.. image:: https://img.shields.io/pypi/v/pyxl320.svg
    :target: https://pypi.python.org/pypi/pyxl320/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/dm/pyxl320.svg
    :target: https://pypi.python.org/pypi/pyxl320/
    :alt: Downloads
.. image:: https://img.shields.io/pypi/l/pyxl320.svg
    :target: https://pypi.python.org/pypi/pyxl320/
    :alt: License

This is still a work in progress and **only** supports XL-320 and **only**
version 2.0 of their protocol. 

.. image:: https://github.com/walchko/pyxl320/blob/master/pics/xl-320.jpg
	:align: center
	
The library is divided up as follows:

 - pyxl320
 	- **ServoSerial** - half duplex hardware serial interface
	- **DummySerial** - for testing, doesn't talk to any hardware
	- **Packet** - creates packets
	- **utils** - misc
	- **xl320** - register/command/error definitions for Dynamixel's XL-320 servo

Not everything is implemented, but more will be added over time.

Setup
--------

Install
~~~~~~~~~~~~~

::

	pip install pyxl320

Development
~~~~~~~~~~~~~

To submit git pulls, clone the repository and set it up as follows:

::

	git clone https://github.com/walchko/pyxl320
	cd pyxl320
	pip install -e .

Usage
--------

.. code:: python

	from pyxl320 import xl320
	from pyxl320 import ServoSerial, Packet, utils

	serial = ServoSerial('/dev/tty.usbserial')  # tell it what port you want to use
	serial.open()

	pkt = Packet.makeServoPacket(1, 158.6)  # move servo 1 to 158.6 degrees
	serial.write(pkt)  # send packet to servo
	ans = serial.read()  # get return status packet

	if packet.isError(ans):
		pkt = packet.makeLEDPacket(1, pyxl320.XL320_LED_RED)
		serial.write(pkt)
		raise Exception('servo error: {}'.format(packet.errorString(ans)))

Al though I have made some packet creators (like LED and Servo), you can make
your own using the basic ``makeWritePacket`` and ``makeReadPacket``.

.. code:: python

	from pyxl320 import Packet, xl320
	from pyxl320.Packet import le  # creates little endian numbers

	# let's make our own servo packet that sends servo 3 to 220.1 degrees
	ID = 3
	reg = xl320.XL320_GOAL_POSITION
	params = le(int(220.1/300*1023))  # convert 220.1 degrees to an int between 0-1023
	pkt = Packet.makeWritePacket(ID, reg, params)


Packet Basics
---------------

======================== === ============== =========== ================================ ===============
Header                   ID  Length         Instruction Parameter                        CRC
======================== === ============== =========== ================================ ===============
[0xFF, 0xFF, 0xFD, 0x00] ID  [LEN_L, LEN_H] INST        [PARAM 1, PARAM 2, ..., PARAM N] [CRC_L, CRC_H]
======================== === ============== =========== ================================ ===============

A status packet back from the servo follows the same format, but the instruction
is always ``0x55`` and maybe followed by error codes if something is wrong.
The length of the packet is aways the entire length minus header, id, and crc.
Also remember, the packets are little-endian, so place numbers in the packet
as ``[LSB, MSB]``. You can use the function ``le()`` in ``Packet`` to accomplish
this.

See the references below for more details on the instructions, error codes, etc.

Hardware
---------

.. image:: https://github.com/walchko/pyxl320/blob/master/pics/xl320_2.png
	:align: center

.. image:: https://github.com/walchko/pyxl320/blob/master/pics/circuit.png
	:align: center

References:
-------------

Unfortunately the Dynamixel references below are **not written well** (many typos
and errors throughout), so please be careful or you will exhibit much frustration.

- `XL-320 e-Manual <http://support.robotis.com/en/product/dynamixel/x_series/xl-320.htm>`_
- `XL-320 hardware and half duplex circuit <http://support.robotis.com/en/product/dynamixel/xl-320.htm>`_
- `Dynamixel Protocol Ver. 2 <http://support.robotis.com/en/product/dynamixel_pro/communication/instruction_status_packet.htm>`_
- `PySerial <http://pyserial.readthedocs.io/en/latest/index.html>`_

ToDo
------

- look at using python ``struct`` for packets
- clean up packet reading, sometimes get a ``0`` appended at beginning or end
- look at using a class system instead of functions for packets
- look at setting up a servo based on a json file
- more helper functions in ``utils`` and or ``bin``

Change Log
-------------

========== ======= =============================
2016-09-05 0.5.0   published to PyPi
2016-08-16 0.0.1   init
========== ======= =============================
