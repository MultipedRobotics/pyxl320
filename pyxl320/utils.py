#!/usr/bin/env python

from Packet import makePingPacket
# import serial
from ServoSerial import ServoSerial


# def hex_decode(data):
# 	"""
# 	b'@ab' -> '0x40 0x61 0x62'
# 	"""
# 	return ((''.join('0x{:02X} '.format(ord(b)) for b in serial.iterbytes(data))), len(data))


def hex_decode(data):
	"""
	in: data - array of numbers [1,2,33,42,234]
	out: str - '0x1 0x02 0x21 0x2a 0xea'
	"""
	return ''.join(map('0x{:02X} '.format, data))


def handleReturn(ans):
	if len(ans) > 0:
		if len(ans) == 1 and ans[0] == chr(0x00):
			print('No returned packet')
		else:
			print('Returned packet[{}]'.format(len(ans)))
			print('array:', hex_decode(ans))
	else:
		print('No returned packet')


def sweep(port, maximum=253):
	"""
	Make this into a better commandline utility
	"""
	s = ServoSerial(port)
	s.open()
	for Id in range(0, maximum):
		pkt = makePingPacket(Id)
		print('ID:', Id, 'pkt:', pkt)
		s.write(pkt)
		ret = s.read()
		handleReturn(ret)
	s.close()

def prettyPrintServo(ID, ctrl_table):
	"""
	This will pretty print out a servo's registers
	"""
	for key, value in ctrl_table:
		print("{:.<29} {}".format(key, value))
