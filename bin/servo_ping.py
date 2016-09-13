#!/usr/bin/env python
from __future__ import print_function
from pyxl320.Packet import makePingPacket, packetToDict
from pyxl320 import ServoSerial
# from pyxl320 import DummySerial
from pyxl320 import utils
import argparse


def sweep(port, rate):
	"""
	Sends a ping packet to ID's from 0 to maximum and prints out any returned
	messages.
	"""
	s = ServoSerial(port, rate)
	# s = DummySerial(port, rate)
	s.open()
	for ID in range(0, 253):
		pkt = makePingPacket(ID)
		s.write(pkt)
		ans = s.read()

		if ans:
			servo = packetToDict(ans)
			utils.prettyPrintPacket(servo)
			print('raw pkt: {}'.format(ans))

	s.close()


def handleArgs():
	parser = argparse.ArgumentParser(description='ping servos')
	parser.add_argument('-r', '--rate', help='servo baud rate', type=int, default=1000000)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/tty.usbserial-A5004Flb')

	args = vars(parser.parse_args())
	return args


if __name__ == '__main__':
	args = handleArgs()
	sweep(args['port'], args['rate'])
