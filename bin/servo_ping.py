#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Send ping commands to all servos

from __future__ import print_function
from pyxl320.Packet import makePingPacket
from pyxl320 import ServoSerial
# from pyxl320 import DummySerial
from pyxl320 import utils
import argparse
import time
from pyxl320 import xl320
from pyxl320.xl320 import ErrorStatusMsg
from serial import SerialException
import sys


def packetToDict(pkt):
	"""
	Given a packet, this turns it into a dictionary ... is this useful?

	in: packet, array of numbers
	out: dictionary (key, value)
	"""

	d = {
		'id': pkt[4],
		# 'instruction': xl320.InstrToStr[pkt[7]],
		# 'length': (pkt[6] << 8) + pkt[5],
		# 'params': pkt[8:-2],
		'Model Number': (pkt[10] << 8) + pkt[9],
		'Firmware Ver': pkt[11],
		'Error': ErrorStatusMsg[pkt[8]],
		# 'crc': pkt[-2:]
	}

	return d


def sweep(port, rate, ID, retry=3):
	"""
	Sends a ping packet to ID's from 0 to maximum and prints out any returned
	messages.

	Actually send a broadcast and will retry (resend) the ping 3 times ...
	"""
	if port == 'dummy':
		s = ServoSerial(port, rate, fake=True)
	else:
		s = ServoSerial(port, rate)

	if ID < 0:
		ID = xl320.XL320_BROADCAST_ADDR

	try:
		s.open()
	except SerialException as e:
		# print('Error opening serial port:')
		print('-'*40)
		print(sys.argv[0], ':')
		print(e)
		exit(1)

	pkt = makePingPacket(ID)
	# print('ping', pkt)
	s.write(pkt)

	# as more servos add up, I might need to increase the cnt number???
	for cnt in range(retry):
		ans = s.read()

		if ans:
			for pkt in ans:
				servo = packetToDict(pkt)
				utils.prettyPrintPacket(servo)
				print('raw pkt: {}'.format(pkt))
		else:
			print('Try {}: no servos found'.format(cnt))

		time.sleep(0.1)

	s.close()


DESCRIPTION = """
Sends out a ping packet and prints all of the returned packets. If you don't
specify a specific id number, the program defaults to 'all'.

Example:

./servo_ping.py /dev/tty.usbserial-AL034G2K
Finding all servos:
Opened /dev/tty.usbserial-AL034G2K @ 1000000
---------------------------------------
id........................... 1
Firmware Ver................. 29
Model Number................. 350
Error........................ None
raw pkt: [255, 255, 253, 0, 1, 7, 0, 85, 0, 94, 1, 29, 31, 71]
---------------------------------------
id........................... 2
Firmware Ver................. 29
Model Number................. 350
Error........................ None
raw pkt: [255, 255, 253, 0, 2, 7, 0, 85, 0, 94, 1, 29, 21, 119]
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	# parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	parser.add_argument('-r', '--rate', help='servo baud rate', type=int, default=1000000)
	parser.add_argument('-i', '--id', help='ping servo ID', type=int, default=-1)
	parser.add_argument('port', help='serial port name, set to "dummy" for testing', type=str)

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	args = handleArgs()
	print('Finding all servos:')
	sweep(port=args['port'], rate=args['rate'], ID=args['id'])
