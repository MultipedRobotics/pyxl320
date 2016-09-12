#!/usr/bin/env python
from __future__ import print_function
from pyxl320.Packet import makePingPacket, prettyPrintPacket, packetToDict
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
from pyxl320 import utils


def sweep(port, maximum=250):
	"""
	Sends a ping packet to ID's from 0 to maximum and prints out any returned
	messages.
	"""
	# s = ServoSerial(port)
	s = DummySerial(port)
	s.open()
	for ID in range(0, maximum):
		pkt = makePingPacket(ID)
		s.write(pkt)
		ans = s.read()

		if ans:
			servo = packetToDict(ans)
			utils.prettyPrintServo(servo)
			print('raw pkt: {}'.format(ans))

	s.close()


if __name__ == '__main__':
	port = '/dev/tty.usbserial-A5004Flb'
	sweep(port)
