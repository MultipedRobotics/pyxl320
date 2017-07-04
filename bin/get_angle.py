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

	# since all servo angles have the same register addr (XL320_GOAL_POSITION)
	# and data size (2), a sinc packet is smart choice
	# compare bulk vs sync for the same commands:
	# bulk = 94 bytes
	# sync = 50 bytes
	# data.append(addr[0])  # LSB
	# data.append(addr[1])  # MSB
	# data.append(2)  # data size LSM
	# data.append(0)  # data size MSB
	# for pkt in info:
	# 	data.append(pkt[0])  # ID
	# 	angle = le(int(pkt[1]/300*1023))
	# 	data.append(angle[0])  # LSB
	# 	data.append(angle[1])  # MSB

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
	parser = argparse.ArgumentParser(description='Sets a servo to an angle')
	parser.add_argument('-i', '--id', help='servo id', type=int, default=-1)
	parser.add_argument('port', help='serial port  or \'dummy\' for testing', type=str)
	# parser.add_argument('angle', help='servo angle in degrees: 0.0 - 300.0', type=float)

	args = vars(parser.parse_args())
	return args


# def main():
# 	args = handleArgs()
#
# 	# if int(args['id']) < 0:
# 	# 	ID = xl320.XL320_BROADCAST_ADDR
# 	# else:
# 	# 	ID = int(args['id'])
#
# 	port = args['port']  # '/dev/tty.usbserial-A5004Flb'
# 	# angle = args['angle']
#
# 	print('Getting servo(s) info on port {}'.format(port))
#
# 	if port.lower() == 'dummy':
# 		s = ServoSerial(port=port, fake=True)
# 	else:
# 		s = ServoSerial(port=port)
# 	s.open()
#
# 	ids = range(1, 3)
# 	# pkt = makeReadPacket(ID, 0x37, le(2))  # read 2 bytes from 0x37 (current angle) register
# 	pkt = makeSyncReadPacket(37, 2, ids)
#
# 	print('made packet:', pkt)
# 	s.write(pkt)
# 	time.sleep(0.01)
#
# 	retry = 3
#
# 	resp = {}
# 	for k in ids:
# 		resp[k] = None
#
# 	# as more servos add up, I might need to increase the cnt number???
# 	for cnt in range(retry):
# 		ans = s.read()
#
# 		if ans:
# 			for pkt in ans:
# 				# servo = packetToDict(pkt)
# 				# utils.prettyPrintPacket(servo)
# 				instr = pkt[7]
# 				err = pkt[8]
# 				print('error:', err, 'instr [0x55]', instr == 0x55)
# 				ID = pkt[4]
# 				angle = float((pkt[10] << 8) + pkt[9])/1023
# 				angle *= 300.0
# 				print('id, angle', ID, angle)
# 				print('raw pkt recv: {}'.format(pkt))
# 				resp[ID] = angle
# 		else:
# 			print('Try {}: no servos found'.format(cnt))
#
# 		time.sleep(0.1)
#
# 	print('resp:', resp)
#
# 	s.close()

def main():
	args = handleArgs()

	# if int(args['id']) < 0:
	# 	ID = xl320.XL320_BROADCAST_ADDR
	# else:
	# 	ID = int(args['id'])

	port = args['port']  # '/dev/tty.usbserial-A5004Flb'
	# angle = args['angle']

	print('Getting servo(s) info on port {}'.format(port))

	if port.lower() == 'dummy':
		s = ServoSerial(port=port, fake=True)
	else:
		s = ServoSerial(port=port)
	s.open()

	ids = range(1, 13)

	# retry = 3

	resp = {}
	for k in ids:
		resp[k] = None

	# as more servos add up, I might need to increase the cnt number???
	for i in ids:
		pkt = makeReadPacket(i, 37, le(2))
		# print('made packet:', pkt)
		ans = s.sendPkt(pkt)

		if ans:
			ans = ans[0]
			# print('returned pkt:', ans)
			ID = ans[4]
			angle = float((ans[10] << 8) + ans[9])/1023
			angle *= 300.0
			# print('id:', ID, 'angle:', angle)
			resp[ID] = angle

		# for cnt in range(retry):
		# 	time.sleep(0.01)
		# 	ans = s.read()
		#
		# 	if ans:
		# 		for pkt in ans:
		# 			# servo = packetToDict(pkt)
		# 			# utils.prettyPrintPacket(servo)
		# 			instr = pkt[7]
		# 			err = pkt[8]
		# 			print('error:', err, 'instr [0x55]', instr == 0x55)
		# 			ID = pkt[4]
		# 			angle = float((pkt[10] << 8) + pkt[9])/1023
		# 			angle *= 300.0
		# 			print('id, angle', ID, angle)
		# 			print('raw pkt recv: {}'.format(pkt))
		# 			resp[ID] = angle
		# 			break
		# 	else:
		# 		print('Try {}: no response found'.format(cnt))

	pprint(resp)

	s.close()


if __name__ == '__main__':
	main()
