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
from pyxl320 import ServoSerial, Packet, xl320
# from pyxl320 import DummySerial
import argparse
import sys
PY3 = sys.version_info > (3,)


def get_input(s):
	"""Handle difference between py2 and py3"""
	if PY3:
		return input(s)
	else:
		return raw_input(s)


def makeServoIDPacket(curr_id, new_id):
	"""
	Given the current ID, returns a packet to set the servo to a new ID
	"""
	pkt = Packet.makeWritePacket(curr_id, xl320.XL320_ID, [new_id])
	return pkt


def makeInterActive():
	port = get_input('Enter serial port >> ')
	curr_id = get_input('Enter current id >> ')
	new_id = get_input('Enter new id >> ')
	return port, curr_id, new_id


def handleArgs():
	parser = argparse.ArgumentParser(description='set servo id')
	parser.add_argument('-i', '--interactive', help='input via commandline', action='store_true')
	parser.add_argument('-n', '--new_id', help='set new id', type=int, default=1)
	parser.add_argument('-c', '--current_id', help='current id', type=int, default=1)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/tty.usbserial-A5004Flb')

	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	if args['interactive']:
		port, curr_id, new_id = makeInterActive()
	else:
		port = args['port']
		curr_id = args['current_id']
		new_id = args['new_id']

	if port == 'dummy':
		ser = ServoSerial(port=port, fake=True)
	else:
		ser = ServoSerial(port=port)
	ser.open()

	pkt = makeServoIDPacket(curr_id, new_id)
	print('pkt', pkt)

	err, err_str = ser.sendPkt(pkt)
	if err:
		print('Error: {} {}'.format(err, err_str))

if __name__ == '__main__':
	main()
