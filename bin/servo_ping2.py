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
from pyxl320 import utils
import argparse
import time
# from pyxl320 import xl320


class ServoPing(ServoSerial):
	"""
	Useful???

	this might replace the function below
	"""
	def __init__(self, port, rate):
		ServoSerial.__init__(self, port, rate)
		self.open()
		self.db = {}

	def ping(self, ID):
		pkt = makePingPacket(ID)
		# self.write(pkt)
		cnt = 3
# 		time.sleep(1)
		while cnt:
			self.write(pkt)
			ans = self.readPkts()

			if ans:
				for pkt in ans:
					servo = packetToDict(pkt)
					id = servo['id']
					if id not in self.db:
						self.db[id] = servo
					else:
						print('dup', id)

# 					print('raw pkt: {}'.format(pkt))

			cnt -= 1
			time.sleep(0.1)

	def print(self):
		print('Found: {} servos'.format(len(self.db)))
		print('-------------------------------------')
		for k, v in self.db.items():
			utils.prettyPrintPacket(v)

	def pingRange(self, start, stop):
		for ID in range(start, stop):
			self.ping(ID)
		self.close()

	def pingAll(self):
		# self.ping(xl320.XL320_BROADCAST_ADDR)
		# self.close()
		for i in range(25):
			self.ping(i)
		self.close()


def handleArgs():
	parser = argparse.ArgumentParser(description='ping servos')
	# parser.add_argument('-m', '--max', help='max id', type=int, default=253)
	# parser.add_argument('-a', '--all', help='reset all servos to defaults', action='store_true')
	parser.add_argument('-i', '--id', help='servo id', type=int, default=-1)
	parser.add_argument('-r', '--rate', help='servo baud rate', type=int, default=1000000)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/serial0')

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	args = handleArgs()
	print('Finding all servos:')
	# sweep(args['port'], args['rate'])
	sp = ServoPing(args['port'], args['rate'])

	if args['id'] == -1:
		sp.pingAll()
		sp.print()
	else:
		sp.ping(args['id'])
		sp.print()
