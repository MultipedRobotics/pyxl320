#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# from pyxl320 import Packet
from pyxl320.Packet import makeSyncAnglePacket
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
# from pyxl320 import xl320
# import time


# def makeSyncAnglePacket(info):
# 	"""
# 	Write bulk angle information to servos.
#
# 	info = [[ID, angle], [ID, angle], ...]
# 	"""
# 	addr = Packet.le(xl320.XL320_GOAL_POSITION)
# 	data = []
#
# 	# since all servo angles have the same register addr (XL320_GOAL_POSITION)
# 	# and data size (2), a sinc packet is smart choice
# 	# compare bulk vs sync for the same commands:
# 	# bulk = 94 bytes
# 	# sync = 50 bytes
# 	data.append(addr[0])  # LSB
# 	data.append(addr[1])  # MSB
# 	data.append(2)  # data size LSM
# 	data.append(0)  # data size MSB
# 	for pkt in info:
# 		data.append(pkt[0])  # ID
# 		angle = Packet.le(int(pkt[1]/300*1023))
# 		data.append(angle[0])  # LSB
# 		data.append(angle[1])  # MSB
#
# 	ID = xl320.XL320_BROADCAST_ADDR
# 	instr = xl320.XL320_SYNC_WRITE
# 	pkt = Packet.makePacket(ID, instr, None, data)  # create packet
#
# 	print(pkt)
#
# 	return pkt


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
	[1, 150.],
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

pkt = makeSyncAnglePacket(data)
serial.sendPkt(pkt)

serial.close()
