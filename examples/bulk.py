#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from pyxl320 import Packet
# from pyxl320 import ServoSerial
from pyxl320 import DummySerial
from pyxl320 import xl320


def makeBulkAnglePacket(info):
	"""
	Write bulk angle information to servos.

	info = [[ID, angle], [ID, angle], ...]
	"""
	addr = Packet.le(xl320.XL320_GOAL_POSITION)
	data = []
	for pkt in info:
		data.append(pkt[0])  # ID
		data.append(addr[0])  # LSB
		data.append(addr[1])  # MSB
		data.append(2)
		data.append(0)
		angle = Packet.le(int(pkt[1]/300*1023))
		data.append(angle[0])  # LSB
		data.append(angle[1])  # MSB

	ID = xl320.XL320_BROADCAST_ADDR
	instr = xl320.XL320_BULK_WRITE
	pkt = Packet.makePacket(ID, instr, None, data)  # create packet

	print(pkt)

	return pkt


port = '/dev/tty.usbserial-A700h2xE'

# serial = ServoSerial(port)  # use this if you want to talk to real servos
serial = DummySerial(port)  # use this for simulation
serial.open()

data = [
	[1, 150],
	[2, 150+45],
	[3, 150+45],
	[4, 150],
	[5, 150+45],
	[6, 150+45],
	[7, 150],
	[8, 150+45],
	[9, 150+45],
	[10, 150],
	[11, 150+45],
	[12, 150+45],
]

pkt = makeBulkAnglePacket(data)
serial.write(pkt)  # there is no returned status packet, so just write
