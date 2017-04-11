#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Send ping commands to all servos

from __future__ import print_function
from pyxl320.Packet import makePingPacket, packetToDict
from pyxl320 import ServoSerial
# from pyxl320 import DummySerial
from pyxl320 import utils
import argparse
import time
from pyxl320 import xl320


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

	s.open()
	pkt = makePingPacket(ID)
	print('ping', pkt)
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


def handleArgs():
	parser = argparse.ArgumentParser(description='ping servos')
	# parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	parser.add_argument('-r', '--rate', help='servo baud rate', type=int, default=1000000)
	parser.add_argument('-i', '--id', help='ping servo ID', type=int, default=-1)
	parser.add_argument('-p', '--port', help='serial port name, set to "dummy" for testing', type=str, default='/dev/serial0')

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	args = handleArgs()
	print('Finding all servos:')
	sweep(port=args['port'], rate=args['rate'], ID=args['id'])
