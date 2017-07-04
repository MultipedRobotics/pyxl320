#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function, division
# from pyxl320 import Packet
from pyxl320 import xl320
from pyxl320 import ServoSerial
from pyxl320.Packet import makeReadPacket, le, makePacket
import argparse
import time
from pprint import pprint


def makeSyncReadPacket(reg, length, ids):
	"""
	Write sync angle information to servos.

	info = [[ID, angle], [ID, angle], ...]
	"""
	# length = le(length)
	data = []

	d = le(reg)
	data.append(d[0])
	data.append(d[1])
	d = le(length)
	data.append(d[0])
	data.append(d[1])
	data += ids

	ID = xl320.XL320_BROADCAST_ADDR
	instr = xl320.XL320_SYNC_READ
	pkt = makePacket(ID, instr, None, data)  # create packet

	# print(pkt)

	return pkt


def handleArgs():
	parser = argparse.ArgumentParser(description='Returns the angles of servos between start and end')
	# parser.add_argument('-i', '--id', help='servo id', type=int, default=-1)
	parser.add_argument('port', help='serial port  or \'dummy\' for testing', type=str)
	parser.add_argument('start', help='starting servo number', type=int)
	parser.add_argument('end', help='ending servo number', type=int)

	# parser.add_argument('angle', help='servo angle in degrees: 0.0 - 300.0', type=float)

	args = vars(parser.parse_args())
	return args

def getInfo(pkt):
	ID = pkt[4]
	angle = float((pkt[10] << 8) + pkt[9])/1023
	angle *= 300.0
	return ID, angle


def getSingle(ID, ser):
	pkt = makeReadPacket(ID, 37, le(2))
	# print('made packet:', pkt)
	ID = None
	angle = None

	ans = ser.sendPkt(pkt)
	if ans:
		ans = ans[0]
		ID, angle = getInfo(ans)

	return ID, angle

def main():
	args = handleArgs()

	# if int(args['id']) < 0:
	# 	ID = xl320.XL320_BROADCAST_ADDR
	# else:
	# 	ID = int(args['id'])

	port = args['port']  # '/dev/tty.usbserial-A5004Flb'
	# angle = args['angle']

	# print('Getting servo(s) info on port {}'.format(port))

	if port.lower() == 'dummy':
		s = ServoSerial(port=port, fake=True)
	else:
		s = ServoSerial(port=port)
	s.open()

	ids = range(args['start'], args['end'] + 1)

	resp = {}
	for k in ids:
		resp[k] = None

	# as more servos add up, I might need to increase the cnt number???
	for i in ids:
		ID, angle = getSingle(i, s)
		resp[i] = angle

	for _ in range(3):
		for k, v in resp.items():
			if v is None:
				ID, angle = getSingle(k, s)
				# if ID != k:
				# 	print('crap', ID, '!=', k)
				resp[k] = angle

	print('')
	print('Servos: {} - {}'.format(args['start'], args['end']))
	print('-' * 40)
	for k, v in resp.items():
		if v is None:
			print('{:4} | {}'.format(k, 'unknown'))
		else:
			print('{:4} | {:.2f}'.format(k, v))

	s.close()


if __name__ == '__main__':
	main()
