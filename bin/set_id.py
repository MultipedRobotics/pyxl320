#!/usr/bin/env python
# ----------------------------
# Simple tool to change the id number of a servo
#

from __future__ import print_function, division
from pyxl320 import ServoSerial, Packet, xl320
from pyxl320 import DummySerial


def main():
	port = raw_input('Enter serial port >> ')
	# ser = ServoSerial(port)
	ser = DummySerial(port)
	ser.open()

	curr_id = raw_input('Enter current id >> ')
	new_id = raw_input('Enter new id >> ')
	pkt = Packet.makeWritePacket(curr_id, xl320.XL320_ID, [new_id])
	ser.write(pkt)
	ret = ser.read()
	print('ret: {}'.format(ret))

if __name__ == '__main__':
	main()
