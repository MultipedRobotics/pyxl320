#!/usr/bin/env

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
from pyxl320 import DummySerial
import argparse


def handleArgs():
	parser = argparse.ArgumentParser(description='Resets servo(s) to factory defaults')
	parser.add_argument('-a', '--all', help='reset all servos to defaults', action='store_true')
	parser.add_argument('-i', '--id', help='servo id', type=int, default=1)
	parser.add_argument('-l', '--level', help='reset level: 0-reset all, 1-reset all but ID, 2-reset all but ID and baud rate', type=int, default=2)
	# parser.add_argument('-c', '--current_id', help='current id', type=int, default=1)
	parser.add_argument('-p', '--port', help='serial port or \'dummy\' for testing, default is \'/dev/serial0\'', type=str, default='/dev/serial0')

	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	print('<<<<<<<<<< WARNING >>>>>>>>>>>>>')
	print(' You are about to reset your servo(s)')
	while True:
		ans = raw_input(' Continue [y/n] >> ')
		if ans == 'y': break
		if ans == 'n': exit()
		print('please type "y" or "n"')

	port = args['port']

	if args['all']:
		ID = xl320.XL320_BROADCAST_ADDR
	else:
		ID = args['id']

	level = args['level']
	if level == 0:
		level = xl320.XL320_RESET_ALL
	elif level == 1:
		level = xl320.XL320_RESET_ALL_BUT_ID
	elif level == 2:
		level = xl320.XL320_RESET_ALL_BUT_ID_BAUD_RATE
	else:
		print('Sorry you selected an invalid reset level')
		exit()

	if port.lower() == 'dummy':
		ser = DummySerial(port)
	else:
		ser = ServoSerial(port)
	ser.open()

	print('Resetting servo[{}] to {} on port {}'.format(ID, level, port))

	pkt = Packet.makeResetPacket(ID, level)

	err, err_str = ser.sendPkt(pkt)
	if err:
		print('Error: {} {}'.format(err, err_str))
	else:
		print('Your servo is reset')


if __name__ == '__main__':
	main()
