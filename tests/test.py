##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Tests for continous integration

from __future__ import print_function
from pyxl320.Packet import le, crc16, findPkt, getPacketType
from pyxl320 import Packet
from pyxl320 import xl320
from pyxl320 import ServoSerial

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
#
# error packet: [255, 255, 253, 0, 1, 4, 0, 85, 128, 162, 143]
# non-error packet: [255, 255, 253, 0, 1, 4, 0, 85, 0, 161, 12]
# non-error packet: [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]
# mal-formed non-error packet: [0, 255, 255, 253, 0, 1, 4, 0, 85, 0, 161, 12]
#


def test_error_packet():
	pkt = [255, 255, 253, 0, 1, 4, 0, 85, 0, 161, 12]
	assert getPacketType(pkt) == 0x55
	# pkt = [255, 255, 253, 0, 1, 4, 0, 85, 128, 162, 143]
	# err_num, err_str = getErrorString(pkt)
	# assert err_num == 128  # this isn't right, but i don't understand it


def test_crc16():
	pkt = [0xff, 0xff, 0xfd, 0x00, 0x01, 0x07, 0x00,  0x02, 0x63, 0x02, 0x04, 0x00, 0x1b, 0xf9]
	ans = crc16(pkt[:-2])  # you don't count the crc
	b = le(ans)
	assert b == [0x1b, 0xf9]


def test_find_pkts():
	err = [0, 255, 255, 253, 0, 1, 4, 0, 85, 0, 161, 12, 0, 4, 0, 255, 255, 253, 0, 1, 4, 0, 85, 128, 162, 143, 0, 0]
	pkts = findPkt(err)
	assert len(pkts) == 2

	err = [0, 1, 4, 0, 85, 0, 161, 12, 0, 4, 0, 255, 255, 253]
	pkts = findPkt(err)
	assert len(pkts) == 0


# these compare built packages to correct packages

def packet_check(a, b):
	assert len(a) == len(b)
	for aa, bb in zip(a, b):
		assert aa == bb


def test_reset_packet():
	ans = [255, 255, 253, 0, 1, 4, 0, 6, 1, 161, 230]
	pkt = Packet.makeResetPacket(1, xl320.XL320_RESET_ALL_BUT_ID)
	packet_check(ans, pkt)


def test_ping_packet():
	ans = [255, 255, 253, 0, 254, 3, 0, 1, 49, 66]
	pkt = Packet.makePingPacket(xl320.XL320_BROADCAST_ADDR)
	packet_check(ans, pkt)


def test_reboot_packet():
	ans = [255, 255, 253, 0, 1, 3, 0, 8, 47, 78]
	pkt = pkt = Packet.makeRebootPacket(1)
	packet_check(ans, pkt)


def test_angle_packet():
	ans = [255, 255, 253, 0, 1, 7, 0, 3, 30, 0, 139, 1, 83, 255]
	pkt = Packet.makeServoPacket(1, 116)
	packet_check(ans, pkt)


def test_led_packet():
	ans = [255, 255, 253, 0, 1, 6, 0, 3, 25, 0, 1, 47, 98]
	pkt = Packet.makeLEDPacket(1, xl320.XL320_LED_RED)
	packet_check(ans, pkt)


# def test_serial():
# 	s = ServoSerial(port='test', fake=True)
# 	s.open()
# 	pkt = Packet.makePingPacket(xl320.XL320_BROADCAST_ADDR)
# 	s.write(pkt)
# 	s.close()
# 	assert True
