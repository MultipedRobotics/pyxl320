#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# ----------------------------
# Simple tool to change the id number of a servo
#

from __future__ import print_function, division
from pyxl320 import ServoSerial
from pyxl320 import Packet
from pyxl320 import xl320
# from pyxl320 import DummySerial
import argparse


def handleArgs():
	parser = argparse.ArgumentParser(description='Resets servo(s) to factory defaults')
	parser.add_argument('-a', '--all', help='reset all servos to defaults', action='store_true')
	parser.add_argument('-i', '--id', help='servo id', type=int, default=1)
	parser.add_argument('-p', '--port', help='serial port or \'dummy\' for testing, default is \'/dev/serial0\'', type=str, default='/dev/serial0')

	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	port = args['port']

	if args['all']:
		ID = xl320.XL320_BROADCAST_ADDR
	else:
		ID = args['id']

	if port.lower() == 'dummy':
		ser = ServoSerial(port=port, fake=True)
	else:
		ser = ServoSerial(port=port)
	ser.open()

	pkt = Packet.makeRebootPacket(ID)
	# print('pkt', pkt)

	ser.write(pkt)
	gramar = 'is'
	if ID == xl320.XL320_BROADCAST_ADDR:
		ID = 'all'
		gramar = 'are'
	print('Servo[{}] {} rebooting'.format(ID, gramar))


if __name__ == '__main__':
	main()
