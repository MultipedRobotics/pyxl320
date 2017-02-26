#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# from pyxl320 import Packet
from pyxl320.Packet import makeSyncAnglePacket
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
import sys
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

if len(sys.argv) != 2:
	print(sys.argv[0], 'needs an angle (degrees): sync.py 200')
	exit()

angle = float(sys.argv[1])

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
	[1, angle],
	[2, angle],
	[3, angle],

	[4, angle],
	[5, angle],
	[6, angle],

	[7, angle],
	[8, angle],
	[9, angle],

	[10, angle],
	[11, angle],
	[12, angle],
]

pkt = makeSyncAnglePacket(data)
serial.sendPkt(pkt)

serial.close()
