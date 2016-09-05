#!/usr/bin/env python

from pyxl320.Packet import goodPacket, isStatusPacket
# from utils import goodPacket

def test_error_packet():
	# pkt = [0, 255, 255, 253, 0, 1, 4, 0, 85, 0, 161, 12]
	pkt = [255, 255, 253, 0, 1, 4, 0, 85, 0, 161, 12]
	assert isStatusPacket(pkt)


def test_crc16():
	# nosetests -v ml-320.py
	# http://forums.trossenrobotics.com/showthread.php?7489-Hard-Can-anyone-give-me-a-sample-packet-by-running-function-quot-Reading-Current-Position-quot-for-Dynamixel-Pro-Motors
	# [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
	# ----headers------
	# 0xff 0xff 0xfd 0x00
	# ----ID----
	# 0x01
	# ----Length----
	# 0x07 0x00
	# ----INST=READ----
	# 0x02
	# ----Address----
	# 0x63 0x02
	# ----Data Length---
	# 0x04 0x00
	# ----CRC_L -> CRC_H-----
	# 0x1B 0xF9
	# pro: current position is reg: 611 = (0x02<<8)+0x63 and is 4 bytes long
	#     [ header	       | res |  ID |  len	   | inst |  param1   | param 2   ]
	pkt = [0xff, 0xff, 0xfd, 0x00, 0x01, 0x07, 0x00,  0x02, 0x63, 0x02, 0x04, 0x00, 0x1b, 0xf9]
	# ans = crc16(buf)
	# b = le(ans)
	# # print('test dec(27,249)', b)
	# # assert b[0] == 0x1B and b[1] == 0xF9
	# assert b == [0x1b, 0xf9]
	assert goodPacket(pkt)

def test_ret_packet():
	# a returned packet from a servo set goal cmd packet
	# FF FF FD 00 01 04 00 55 00 A1 0C
	pkt = [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]
	# pcrc = pkt[-2:]
	# crc = crc16(pkt[:-2])
	# assert pcrc == le(crc)
	assert goodPacket(pkt)

def test_status_packet():
	pkt = [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]
	assert isStatusPacket(pkt)
