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
# import time
from pyxl320 import xl320


class ServoPing(ServoSerial):
	"""
	Useful???

	this might replace the function below
	"""
	def __init__(self, port, rate):
		ServoSerial.__init__(self, port, rate)
		self.open()

	def ping(self, ID):
		pkt = makePingPacket(ID)
		ret = self.sendPkt(pkt, 3)  # not sure if I need 3 retries on the packet
		if ret:
			print('---------------------------------------------')
			servo = packetToDict(ret)
			utils.prettyPrintPacket(servo)
			print('raw pkt: {}'.format(ret))

	def pingRange(self, start, stop):
		for ID in range(start, stop):
			self.ping(ID)
		self.close()

	def pingAll(self):
		self.ping(xl320.XL320_BROADCAST_ADDR)
		self.close()


def sweep(port, rate, retry=3):
	"""
	Sends a ping packet to ID's from 0 to maximum and prints out any returned
	messages.

	Actually send a broadcast and will retry (resend) the ping 3 times ...
	"""
	s = ServoSerial(port, rate)
	# s = DummySerial(port, rate)

	s.open()
	pkt = makePingPacket(xl320.XL320_BROADCAST_ADDR)
	s.write(pkt)
	s.write(pkt)

	# as more servos add up, I might need to increase the cnt number???
	cnt = retry
	while cnt:
		ans = s.readPkts()

		if ans:
			for pkt in ans:
				servo = packetToDict(pkt)
				utils.prettyPrintPacket(servo)
				print('raw pkt: {}'.format(pkt))
		# else:
		# 	print('cnt {} not found'.format(cnt))

		cnt -= 1

	s.close()


def handleArgs():
	parser = argparse.ArgumentParser(description='ping servos')
	# parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	parser.add_argument('-r', '--rate', help='servo baud rate', type=int, default=1000000)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/tty.usbserial-A5004Flb')

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	args = handleArgs()
	print('Finding all servos:')
	sweep(args['port'], args['rate'])
