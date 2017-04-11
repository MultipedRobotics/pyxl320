#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# ---------------------------
# Set servo properties according to a json file
#
# Note: the servo ID's must already be set, this can't do it with multiple
# servos connected. If only one, then it can.

from __future__ import print_function, division
# from pyxl320 import DummySerial
from pyxl320 import ServoSerial
# from pyxl320 import Packet, xl320
from pyxl320 import Packet
# from pyxl320.Packet import le
# import simplejson as json
from pyxl320.utils import JsonFile

# is there a better way?
# key: {[regisiter, data_size]}
# xl320_reg = {
# 	"XL320_ID": [xl320.XL320_ID],
# 	"XL320_CW_ANGLE_LIMIT": [xl320.XL320_CW_ANGLE_LIMIT, 2, Packet.makeServoMinLimitPacket],
# 	"XL320_CCW_ANGLE_LIMIT": [xl320.XL320_CCW_ANGLE_LIMIT, 2, Packet.makeServoMaxLimitPacket],
# 	# "XL320_TORQUE_ENABLE": [xl320.XL320_TORQUE_ENABLE, 1],
# 	# "XL320_LED": [xl320.XL320_LED, 1],
# 	"XL320_GOAL_POSITION": [xl320.XL320_GOAL_POSITION, 2, Packet.makeServoPacket],
# 	"XL320_GOAL_VELOCITY": [xl320.XL320_GOAL_VELOCITY, 2, Packet.makeServoSpeedPacket],
# }

xl320_func = {
	"min_angle": [Packet.makeServoMinLimitPacket],
	"max_angle": [Packet.makeServoMaxLimitPacket],
	"set_angle": [Packet.makeServoPacket],
	"speed_limit": [Packet.makeServoSpeedPacket],
	"led": [Packet.makeLEDPacket]
}

data = JsonFile.read('test.json')
print(data)


def main():
	filename = 'test.json'
	port = '/dev/tty.usbserial0'

	data = JsonFile.read(filename)
	print(data)

	if port == 'dummy':
		ser = ServoSerial(port=port, fake=True)
	else:
		ser = ServoSerial(port=port)
	
	ser.open()

	for servo in data:
		ID = servo['id']
		servo.pop('id')
		for key, val in servo.items():
			print('> setting servo[{}]: {} {}'.format(ID, key, val))

			if key in xl320_func:
				func = xl320_func[key][0]  # grab correct function
				pkt = func(ID, val)  # build packet
				# print('pkt', pkt)
				ser.sendPkt(pkt)  # send packet

			else:
				print('>> Error: {} not currently supported'.format(key))


if __name__ == '__main__':
	main()
