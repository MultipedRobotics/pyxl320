#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from pyxl320.Packet import makeSyncAnglePacket
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
import sys


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
