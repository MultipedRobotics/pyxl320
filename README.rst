pyXL320
=========

.. image:: https://landscape.io/github/walchko/pyxl320/master/landscape.svg?style=flat
   :target: https://landscape.io/github/walchko/pyxl320/master
   :alt: Code Health
.. image:: https://img.shields.io/pypi/v/pyxl320.svg
    :target: https://pypi.python.org/pypi/pyxl320/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/l/pyxl320.svg
    :target: https://pypi.python.org/pypi/pyxl320/
    :alt: License
.. image:: https://travis-ci.org/walchko/pyxl320.svg?branch=master
    :target: https://travis-ci.org/walchko/pyxl320

This is still a work in progress and **only** supports XL-320 and **only**
version 2.0 of their protocol.

.. image:: https://raw.githubusercontent.com/walchko/pyxl320/master/pics/xl-320.jpg
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

.. image:: https://raw.githubusercontent.com/walchko/pyxl320/master/pics/green.jpg
	:align: center

A simple example to turn the servo and turn the LED to green:

.. code-block:: python

	from pyxl320 import xl320
	from pyxl320 import ServoSerial, Packet, utils

	serial = ServoSerial('/dev/tty.usbserial')  # tell it what port you want to use
	serial.open()

	pkt = Packet.makeServoPacket(1, 158.6)  # move servo 1 to 158.6 degrees
	err_num, err_str = serial.sendPkt(pkt)  # send packet to servo

	if err_num:
		raise Exception('servo error: {}'.format(err_str)

	pkt = packet.makeLEDPacket(1, pyxl320.XL320_LED_GREEN)
	serial.sendPkt(pkt)


Although I have made some packet creators (like LED and Servo), you can make
your own using the basic ``makeWritePacket`` and ``makeReadPacket``.

.. code-block:: python

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

.. image:: https://raw.githubusercontent.com/walchko/pyxl320/master/pics/xl320_2.png
	:align: center

.. image:: https://raw.githubusercontent.com/walchko/pyxl320/master/pics/circuit.png
	:align: center

.. image:: https://raw.githubusercontent.com/walchko/pyxl320/master/pics/servo_angles.png
	:align: center

I have used the `74LS241 <http://savageelectronics.blogspot.com/2011/01/arduino-y-dynamixel-ax-12.html>`_
to talk to the xl-320.

References:
-------------

Unfortunately the Dynamixel references below are **not written well** (many typos
and errors throughout), so please be careful or you will exhibit much frustration.
Also they have disappeared at times, so if you get a ``404`` error, hopefully they
will come back.

- `XL-320 e-Manual <http://support.robotis.com/en/techsupport_eng.htm#product/actuator/dynamixel_x/xl_series/xl-320.htm>`_
- `XL-320 hardware and half duplex circuit <http://support.robotis.com/en/product/actuator/dynamixel_x/xl-series_main.htm>`_
- `Dynamixel Protocol Ver. 2 <http://support.robotis.com/en/product/dynamixel_pro/communication/instruction_status_packet.htm>`_
- `PySerial <http://pyserial.readthedocs.io/en/latest/index.html>`_

ToDo
-----

- bulk read/write
- sync read/write

Change Log
-------------

========== ======= =============================
2016-10-11 0.7.1   small changes/updates
2016-09-12 0.7.0   refactoring, still working on API
2016-09-05 0.5.0   published to PyPi
2016-08-16 0.0.1   init
========== ======= =============================

License
----------

The MIT License (MIT)
Copyright (c) 2016 Kevin J. Walchko

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
