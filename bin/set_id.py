#!/usr/bin/env python
# ----------------------------
# Simple tool to change the id number of a servo
#

from __future__ import print_function, division
from pyxl320 import ServoSerial, Packet, xl320
from pyxl320 import DummySerial
import argparse


def makeServoIDPacket(curr_id, new_id):
	"""
	Given the current ID, returns a packet to set the servo to a new ID
	"""
	pkt = Packet.makeWritePacket(curr_id, xl320.XL320_ID, [new_id])
	return pkt


def makeInterActive():
	port = raw_input('Enter serial port >> ')
	curr_id = raw_input('Enter current id >> ')
	new_id = raw_input('Enter new id >> ')
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
		new_id = args['new_d']

	ser = DummySerial(port)
	ser.open()

	makeServoIDPacket(ser, curr_id, new_id)

	ser.write(pkt)
	ret = ser.read()
	print('ret: {}'.format(ret))

if __name__ == '__main__':
	main()
