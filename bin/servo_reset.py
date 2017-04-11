#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# ----------------------------
# Simple tool to change the id number of a servo
#
# I believe I am doing this correct, but it doesn't work

from __future__ import print_function, division
from pyxl320 import ServoSerial
from pyxl320 import Packet
from pyxl320 import xl320
# from pyxl320 import DummySerial
from pyxl320 import utils
from time import sleep
import argparse
import sys
PY3 = sys.version_info > (3,)


def get_input(s):
	"""Handle difference between py2 and py3"""
	if PY3:
		return input(s)
	else:
		return raw_input(s)


def handleArgs():
	parser = argparse.ArgumentParser(description='Resets servo(s) to factory defaults')
	parser.add_argument('-a', '--all', help='reset all servos to defaults', action='store_true')
	parser.add_argument('-i', '--id', help='servo id', type=int, default=1)
	parser.add_argument('-l', '--level', help='reset level: 0-reset all, 1-reset all but ID, 2-reset all but ID and baud rate', type=int, default=2)
	# parser.add_argument('-c', '--current_id', help='current id', type=int, default=1)
	parser.add_argument('-p', '--port', help='serial port or \'dummy\' for testing, default is \'/dev/serial0\'', type=str, default='/dev/serial0')
	parser.add_argument('-y', '--yes', help='answer "yes" to prompt and force reset', action='store_true')

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	print('<<<< PyXL320 Servo Reset >>>>')
	args = handleArgs()

	if args['yes']:
		pass
	else:
		print('<<<<<<<<<< WARNING >>>>>>>>>>>>>')
		print(' You are about to reset your servo(s)')
		while True:
			ans = get_input(' Continue [y/n] >> ')
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
		ser = ServoSerial(port=port, fake=True)
	else:
		ser = ServoSerial(port=port)
	ser.open()

	pkt = Packet.makeResetPacket(ID, level)

	if args['all']:
		servo_str = 'all servos'
	else:
		servo_str = 'servo ID {}'.format(args['id'])

	if level == xl320.XL320_RESET_ALL:
		level_str = 'all parameters'
	elif level == xl320.XL320_RESET_ALL_BUT_ID:
		level_str = 'all parameters but ID'
	elif level == xl320.XL320_RESET_ALL_BUT_ID_BAUD_RATE:
		level_str = 'all parameters but ID and baudrate'

	print('\nResetting {}: {} set to default'.format(servo_str, level_str))
	ser.write(pkt)
	# print('packet', pkt)
	sleep(1)

	# do a reboot -----------------------------------------------------------
	pkt = Packet.makeRebootPacket(ID)
	ser.write(pkt)
	print('\nYour servo(s) should be reset now')
	sleep(1)

	# maybe include smarter logic than just spamming every servo ------------
	pkt = Packet.makePingPacket(xl320.XL320_BROADCAST_ADDR)
	ser.write(pkt)
	for cnt in range(3):
		ans = ser.read()

		if ans:
			for pkt in ans:
				servo = Packet.packetToDict(pkt)
				utils.prettyPrintPacket(servo)
				print('raw pkt: {}'.format(pkt))
		else:
			print('Try {}: no servos found'.format(cnt))

		sleep(0.1)
