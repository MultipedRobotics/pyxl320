#!/usr/bin/env python
#
# Library tha works with Dynamixel XL-320 servos.
#
#
# Change log:
#	2016-08-16  init
#	2016-09-04  refactor

from __future__ import division, print_function
from xl320 import *

"""
A bunch of packet constructors, file name follows make* and returns a complete
packet (array of ints). The serial class will turn it into an array of bytes using
bytes(bytearray(pkt)) before sending it.

Packet format:

[0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]

Header: 0xFF, 0xFF, 0xFD
Reserved byte: 0x00
Servo ID: ID
Packet Length: Len_l, len_h
Instruction: INST
Parameters: Param 1 ... Param N
CRC: crc_l, crc_h

"""

"""
This code uses:
http://support.robotis.com/en/product/dynamixel_pro/communication/instruction_status_packet.htm
"""
crc_table = [
	0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
	0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
	0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
	0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
	0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
	0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
	0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
	0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
	0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
	0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
	0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
	0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
	0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
	0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
	0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
	0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
	0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
	0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
	0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
	0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
	0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
	0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
	0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
	0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
	0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
	0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
	0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
	0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
	0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
	0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
	0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
	0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
]


def crc16(data_blk):
	"""
	Calculate crc

	in: data_blk - entire packet except last 2 crc bytes
	out: crc_accum - 16 word
	"""
	data_blk_size = len(data_blk)
	crc_accum = 0
	for j in range(data_blk_size):
		i = ((crc_accum >> 8) ^ data_blk[j]) & 0xFF
		crc_accum = ((crc_accum << 8) ^ crc_table[i])
		crc_accum &= 0xffff  # keep to 16 bits

	return crc_accum


def le(h):
	"""
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
	h &= 0xffff  # make sure it is 16 bits
	return [h & 0xff, h >> 8]


def makePacket(ID, instr, reg=None, params=None):
	"""
	This makes a generic packet.

	TODO: look a struct ... does that add value using it?

	0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
	in:
		ID - servo id
		instr - instruction
		reg - register
		params - instruction parameter values
	out: packet
	"""
	pkt = []
	pkt += [0xFF, 0xFF, 0xFD]  # header
	pkt += [0x00]  # reserved byte
	pkt += [ID]
	pkt += [0x00, 0x00]  # length placeholder
	pkt += [instr]  # instruction
	if reg: pkt += le(reg)  # not everything has a register
	if params: pkt += params    # not everything has parameters

	length = le(len(pkt)-5)  # length = len(packet) - (header(3), reserve(1), id(1))
	pkt[5] = length[0]  # L
	pkt[6] = length[1]  # H

	crc = crc16(pkt)
	pkt += le(crc)

	return pkt


def makePingPacket(ID):
	#      | header          | rsv | id| length    |instr|
	# pkt = [0xff, 0xff, 0xfd, 0x00, ID, 0x03, 0x00, 0x01, crc_l, crc_h]
	pkt = makePacket(ID, XL320_PING)
	return pkt


def makeWritePacket(ID, reg, values=None):
	"""
	Creates a packet that writes a value(s) to servo ID at location reg. Make
	sure the values are in little endian (use Packet.le() if necessary) for 16 b
	(word size) values.
	"""
	pkt = makePacket(ID, XL320_WRITE, reg, values)
	return pkt


def makeReadPacket(ID, reg, values=None):
	"""
	Creates a packet that reads the register(s) of servo ID at location reg. Make
	sure the values are in little endian (use Packet.le() if necessary) for 16 b
	(word size) values.
	"""
	pkt = makePacket(ID, XL320_READ, reg, values)
	return pkt


def makeResetPacket(ID, param):
	pkt = makePacket(ID, XL320_RESET, None, param)
	return pkt


def makeRebootPacket(ID):
	pkt = makePacket(ID, XL320_REBOOT)
	return pkt


# [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, 0x30, ANGLE_L, ANGLE_H, CRC_L, CRC_H]
def makeServoPacket(ID, angle):
	if not (0.0 <= angle <= 300.0):
		raise Exception('moveServo(), angle out of bounds: {}'.format(angle))
	val = int(angle/300*1023)
	# lo, hi = le(val)
	# print('servo cmd {} deg : {} : L {} H {}'.format(angle, val, lo, hi))
	pkt = makeWritePacket(ID, XL320_GOAL_POSITION, le(val))
	return pkt

# FIXME: this returns 2 packets, I don't like it
def makeServoLimits(ID, maxAngle, minAngle):
	"""
	"""
	if maxAngle > 300.0 or minAngle < 0.0:
		raise Exception('makeServoLimits: {:.2f}-{:.2f} exceeds limits 0-300 deg'.format(maxAngle, minAngle))
	if minAngle > maxAngle:
		raise Exception('makeServoLimits: maxAngle {:.2f} is larger than minAngle {:.2f}'.format(maxAngle, minAngle))

	pkt1 = makeWritePacket(ID, XL320_CCW_ANGLE_LIMIT, le[maxAngle])
	pkt2 = makeWritePacket(ID, XL320_CW_ANGLE_LIMIT, le[minAngle])

	return pkt1, pkt2


def makeServoSpeed(ID, maxSpeed):
	"""
	Run servo between 0.0 to 1.0, where 1.0 is 100% (full) speed.
	"""
	if 0.0 > maxSpeed > 1.0:
		raise Exception('makeServoSpeed: max speed is a percentage (0.0-1.0)')
	speed = maxSpeed*1023
	pkt = makeWritePacket(ID, XL320_GOAL_VELOCITY, le(speed))
	return pkt


def makeLEDPacket(ID, color):
	# pkt = [255, 255, 253, 0, ID, 11, 0, 3, 25, 0, 2 crc_l, crc_h]
	pkt = makeWritePacket(ID, XL320_LED, [color])
	return pkt


def makeControlModePacket(ID, mode):
	pkt = makeWritePacket(ID, XL320_CONTROL_MODE, le(mode))
	return pkt

# def makeDumpPacket(ID):
# 	pkt = makeReadPacket()


# this is more of a utility
def goodPacket(pkt):
	"""
	Checks to ensure it is a good packet. It checks for:
	proper header
	good crc
	"""
	pcrc = pkt[-2:]  # get crc from packet
	crc = crc16(pkt[:-2])  # calculate crc from packet
	if pcrc == le(crc) and [0xff, 0xff, 0xfd, 0x00] == pkt[:4]:
		return True
	else:
		return False


def isStatusPacket(pkt):
	"""
	Checks to ensure it is a good status packet. It checks for:
	proper header
	good crc
	instruction is XL320_STATUS (0x55)
	"""
	if not goodPacket(pkt): return False
	if pkt[7] == XL320_STATUS: return True
	return False


def isError(pkt):
	if pkt[7] == XL320_STATUS and len(pkt) == 11:
		return False
	else:
		return True


def errorString(pkt):
	# bit 7 - alert
	# bit 0-6 - error number 0-64
	# err_str = {
	# 	0: 'none',
	# 	1: 'result fail',
	# 	2: 'instruction error',
	# 	4: 'crc error',
	# 	8: 'data range error',
	# 	16: 'data length error',
	# 	32: '?',
	# 	64: '?'
	# }
	err_str = [
		'none',
		'result fail',
		'instruction error',
		'crc error',
		'data range error',
		'data length error',
		'?',
		'?'
	]
	ret = err_str[0]
	if pkt[7] == XL320_STATUS and len(pkt) > 11:
		err = pkt[8] | 128  # remove alert bit
		# ret = err_str[err]
		ret = 'error: {}'.format(err)
	return ret


def prettyPrintPacket(pkt):
	s = 'packet ID: {} instr: {} len: {}'.format(pkt[4], pkt[7], int((pkt[6] << 8) + pkt[5]))
	if len(s) > 10:
		params = pkt[8:-2]
		s += ' params: {}'.format(params)
	return s
