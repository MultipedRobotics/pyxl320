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


class ServoBase(object):
	"""
	Does this add value?

	maybe just use servoserial instead?
	"""
	def __init__(self):
		pass

	def open(self, port, rate=1000000):
		self.serial = ServoSerial(port, rate)
		# self.serial = DummySerial(port, rate)

	def close(self):
		self.serial.close()


class ServoInfo(ServoBase):
	def __init__(self):
		pass

	def getInfo(self, ID):
		pkt = None
		ans = self.serial.sendPkt(pkt)
		return ans

	def printInfo(self, ID):
		ans = self.getInfo(ID)
		print(ans)


def sweep(port, rate, max):
	"""
	Sends a ping packet to ID's from 0 to maximum and prints out any returned
	messages.
	"""
	s = ServoSerial(port, rate)
	# s = DummySerial(port, rate)

	s.open()
	pkt = makePingPacket(xl320.XL320_BROADCAST_ADDR)
	s.write(pkt)
	s.write(pkt)

	# as more servos add up, I might need to increase the cnt number???
	cnt = 3
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
	parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	parser.add_argument('-r', '--rate', help='servo baud rate', type=int, default=1000000)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/tty.usbserial-A5004Flb')

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	args = handleArgs()
	sweep(args['port'], args['rate'], args['max'])
