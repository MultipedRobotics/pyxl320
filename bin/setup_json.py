#!/usr/bin/env python
# ---------------------------
# Set servo properties according to a json file
#
# Note: the servo ID's must already be set, this can't do it with multiple
# servos connected. If only one, then it can.

from __future__ import print_function, division
from pyxl320 import DummySerial
from pyxl320 import Packet, xl320
from pyxl320.Packet import le
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


# class JsonFile(object):
# 	"""
# 	Simple class to handle json files.
# 	"""
# 	@staticmethod
# 	def read(fname):
# 		"""
# 		Reads a Json file
# 		in: file name
# 		out: length of file, dictionary
# 		"""
# 		try:
# 			with open(fname, 'r') as f:
# 				data = json.load(f)
# 			return data
#
# 		except IOError:
# 			raise Exception('Could not open {0!s} for reading'.format((fname)))
#
# 	@staticmethod
# 	def write(fname, data):
# 		"""
# 		Writes a Json file
# 		"""
# 		try:
# 			with open(fname, 'w') as f:
# 				json.dump(data, f)
#
# 		except IOError:
# 			raise Exception('Could not open {0!s} for writing'.format((fname)))

# data = {
# 	1: {
# 		"XL320_CW_ANGLE_LIMIT": 200,
# 		"XL320_CCW_ANGLE_LIMIT": 20
# 	},
# 	2: {
# 		"XL320_CW_ANGLE_LIMIT": 200,
# 		"XL320_CCW_ANGLE_LIMIT": 20
# 	}
# }

# data = {
# 	1: {
# 		xl320.XL320_CW_ANGLE_LIMIT: 200,
# 		xl320.XL320_CCW_ANGLE_LIMIT: 20
# 	},
# 	2: {
# 		xl320.XL320_CW_ANGLE_LIMIT: 200,
# 		xl320.XL320_CCW_ANGLE_LIMIT: 20
# 	}
# }

data = JsonFile.read('test.json')
print(data)
# exit()
#
# data = [
# 	{
# 		xl320.XL320_ID: 1,
# 		xl320.XL320_CW_ANGLE_LIMIT: 200,
# 		xl320.XL320_CCW_ANGLE_LIMIT: 20
# 	},
# 	{
# 		xl320.XL320_ID: 2,
# 		xl320.XL320_CW_ANGLE_LIMIT: 200,
# 		xl320.XL320_CCW_ANGLE_LIMIT: 20
# 	}
# ]

def main():
	filename = 'test.json'
	port = 'a'

	ser = DummySerial(port)
	ser.open()

	# jf = JsonFile()
	# data = jf.readJson(filename)



	# print(data)
	# print('xl320.XL320_ID:', data[1][xl320.XL320_ID])
	# exit()

	for servo in data:
		ID = servo['id']
		servo.pop('id')
		for key, val in servo.items():
			print('> setting servo[{}]: {} {}'.format(ID, key, val))

			# reg = key
			# reg = xl320_reg[key][0]
			# if xl320_reg[key][1] == 1:
			# 	param = val
			# else:
			# 	param = val

			# pkt = Packet.makeWritePacket(ID, reg, param)
			if key in xl320_func:
				func = xl320_func[key][0]
				pkt = func(ID, val)
				print('pkt', pkt)
				ser.write(pkt)
				ser.read()
			else:
				print('>> Error: {} not found'.format(key))

			# the servo id changed, so update it
			# if key == 'XL320_ID':
			# 	curr_id = val

if __name__ == '__main__':
	main()
