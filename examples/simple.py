#!/usr/bin/env python

import pyxl320
from pyxl320 import ServoSerial, Packet, xl320
from pyxl320 import DummySerial

serial = DummySerial('/dev/tty.usbserial')  # use this if you want to talk to real servos
# serial = DummySerial('/dev/tty.usbserial')  # tell it what port you want to use
serial.open()

pkt = Packet.makeServoPacket(1, 158.6)  # move servo 1 to 158.6 degrees
serial.write(pkt)  # send packet to servo
ans = serial.read()  # get return status packet

if Packet.isError(ans):
	pkt = Packet.makeLEDPacket(1, xl320.XL320_LED_RED)
	serial.write(pkt)
	raise Exception('servo error: {}'.format(Packet.errorString(ans)))
