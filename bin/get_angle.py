#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function, division
from pyxl320 import ServoSerial
from pyxl320.Packet import le, makeReadPacket
import argparse
import simplejson as json
# from pyxl320.xl320 import ErrorStatusMsg


# def makeSyncReadPacket(reg, length, ids):
# 	"""
# 	Write sync angle information to servos.
#
# 	info = [[ID, angle], [ID, angle], ...]
# 	"""
# 	# length = le(length)
# 	data = []
#
# 	d = le(reg)
# 	data.append(d[0])
# 	data.append(d[1])
# 	d = le(length)
# 	data.append(d[0])
# 	data.append(d[1])
# 	data += ids
#
# 	ID = xl320.XL320_BROADCAST_ADDR
# 	instr = xl320.XL320_SYNC_READ
# 	pkt = makePacket(ID, instr, None, data)  # create packet
#
# 	# print(pkt)
#
# 	return pkt


def writeToFile(data, filename='data.json'):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


DESCRIPTION = """
Returns the angles of servos between <start> and <end>. The servo search range
has to be continous. You can not select servos 1, 3, 6, 7; you have to select
1 - 7.

example: get_angle.py /dev/serial0 1 7

Servos: 1 - 7
   # | Angle
----------------------------------------
   1 | 143.70
   2 | 281.23
   3 |  97.07
   4 | 147.51
   5 | 280.06
   6 | 105.87
   7 | 154.84
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('port', help='serial port  or \'dummy\' for testing', type=str)
	parser.add_argument('start', help='starting servo number', type=int)
	parser.add_argument('end', help='ending servo number', type=int)
	parser.add_argument('-j', '--json', help='save info to a json file, you must supply a file name: --json my_file.json', type=str)

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
	port = args['port']

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
		cnt = 0
		for k, v in resp.items():
			# search through and find servos w/o responses (i.e., None)
			if v is None:
				cnt += 1  # found a None
				ID, angle = getSingle(k, s)
				resp[k] = angle

		if cnt == 0:  # we must have gotten them all on the last run
			break

	print('')
	print('Servos: {} - {}'.format(args['start'], args['end']))
	print('{:>4} | {:6}'.format('#', 'Angle'))
	print('-' * 40)
	for k, v in resp.items():
		if v is None:
			print('{:4} | {}'.format(k, 'unknown'))
		else:
			print('{:4} | {:6.2f}'.format(k, v))
	print('')

	if args['json']:
		print('Saving servo angle info to {}'.format(args['json']))
		writeToFile(resp, args['json'])

	s.close()


if __name__ == '__main__':
	main()
