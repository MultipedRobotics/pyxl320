#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function, division
from pyxl320 import ServoSerial
from pyxl320 import Packet
# from pyxl320 import DummySerial
import argparse

rates = {
	9600: 0,
	57600: 1,
	115200: 2,
	1000000: 3
}


def handleArgs():
	parser = argparse.ArgumentParser(description='set servo buad rate')
	# parser.add_argument('-n', '--newid', help='set new id', type=int, default=1)
	parser.add_argument('-c', '--current_rate', help='current baud rate, default is 1000000', type=int, default=1000000)
	parser.add_argument('-i', '--id', help='current id', type=int, default=1)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='/dev/tty.usbserial-A5004Flb')
	parser.add_argument('-r', '--new_rate', help='set new baud rate to 9600, 57600, 115200, or 1000000; default is 1000000', type=int, default=1000000)

	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	port = args['port']
	ID = args['id']
	curr_rate = args['current_rate']
	# new_id = args['newid']
	# 0: 9600, 1:57600, 2:115200, 3:1Mbps
	new_rate = rates[args['new_rate']]

	if port == 'dummy':
		ser = ServoSerial(port=port, baud_rate=curr_rate, fake=True)
	else:
		ser = ServoSerial(port=port, baud_rate=curr_rate)
	ser.open()

	pkt = Packet.makeBaudRatePacket(ID, new_rate)
	ser.sendPkt(pkt)

	# pkt = Packet.makeRebootPacket(ID)
	# ser.sendPkt(pkt)

if __name__ == '__main__':
	main()
