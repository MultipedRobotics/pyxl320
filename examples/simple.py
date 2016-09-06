#!/usr/bin/env python

import pyxl320
from pyxl320 import ServoSerial
from pyxl320 import Packet, xl320
# from pyxl320 import DummySerial

ID = 1
port = '/dev/tty.usbserial'
angle = 158.6

serial = ServoSerial(port)  # use this if you want to talk to real servos
# serial = DummySerial('/dev/tty.usbserial')  # use this for simulation
serial.open()

pkt = Packet.makeServoPacket(ID, angle)  # move servo 1 to 158.6 degrees
serial.write(pkt)  # send packet to servo
ans = serial.read()  # get return status packet

if Packet.isError(ans):
	# turn LED red
	pkt = Packet.makeLEDPacket(ID, xl320.XL320_LED_RED)
	serial.write(pkt)
	raise Exception('servo error: {}'.format(Packet.errorString(ans)))
