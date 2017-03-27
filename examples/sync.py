#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from pyxl320.Packet import makeSyncAnglePacket
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
import argparse


def handleArgs():
	parser = argparse.ArgumentParser(description='set servos to an angle using sync command')
	parser.add_argument('angle', help='servo angle', type=float, default=150.0)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/serial0')
	# parser.add_argument('-g', '--gpio', help='Raspberry Pi GPIO pin number', type=int, default=17)

	args = vars(parser.parse_args())
	return args


args = handleArgs()
port = args['port']
angle = args['angle']

if port:
	print('Opening: {}'.format(port))
	serial = ServoSerial(port)  # use this if you want to talk to real servos
else:
	print('Using dummy serial port for testing')
	serial = DummySerial(port)  # use this for simulation

serial.open()

data = [
	(1, angle),
	(2, angle),
	(3, angle),

	(4, angle),
	(5, angle),
	(6, angle),

	(7, angle),
	(8, angle),
	(9, angle),

	(10, angle),
	(11, angle),
	(12, angle)
]

pkt = makeSyncAnglePacket(data)
serial.sendPkt(pkt)

serial.close()
