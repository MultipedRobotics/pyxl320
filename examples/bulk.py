#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# from pyxl320.Packet import makeBulkAnglePacket
from pyxl320 import ServoSerial
from pyxl320 import DummySerial


def makeBulkAnglePacket(info):
	"""
	Write bulk angle information to servos.

	info = [[ID, angle], [ID, angle], ...]
	"""
	from pyxl320 import xl320
	from pyxl320 import Packet

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

	return pkt


port = '/dev/serial0'
# port = None

if port:
	print('Opening: {}'.format(port))
	serial = ServoSerial(port)  # use this if you want to talk to real servos
else:
	print('Using dummy serial port for testing')
	serial = DummySerial(port)  # use this for simulation

serial.open()

data = [
	[1, 150],
	[2, 150],
	[3, 150],

	[4, 150],
	[5, 150],
	[6, 150],

	[7, 150],
	[8, 150],
	[9, 150],

	[10, 150],
	[11, 150],
	[12, 150],
]

pkt = makeBulkAnglePacket(data)
serial.write(pkt)  # there is no returned status packet, so just write
#serial.write(pkt)

print('Raw Packet:', pkt)

serial.close()
