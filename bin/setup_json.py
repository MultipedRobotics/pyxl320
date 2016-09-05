#!/usr/bin/env python
# ---------------------------
# Set servo properties according to a json file
#

from __future__ import print_function, division
from pyxl320 import DummySerial
from pyxl320 import Packet, xl320
from pyxl320.Packet import le
import simplejson as json

# is there a better way?
xl320_reg = {
	"XL320_ID": [Packet.XL320_ID, 1],
	"XL320_CW_ANGLE_LIMIT": [xl320.XL320_CW_ANGLE_LIMIT, 2],
	"XL320_CCW_ANGLE_LIMIT": [xl320.XL320_CCW_ANGLE_LIMIT, 2],
	# "XL320_TORQUE_ENABLE": Packet.XL320_TORQUE_ENABLE,
	# "XL320_LED": Packet.XL320_LED,
	# "XL320_GOAL_POSITION": Packet.XL320_GOAL_POSITION,
	# "XL320_GOAL_VELOCITY": Packet.XL320_GOAL_VELOCITY,
	# "XL320_PRESENT_POSITION": Packet.XL320_PRESENT_POSITION,
	# "XL320_PESENT_LOAD": Packet.XL320_PESENT_LOAD,
	# "XL320_PESENT_VOLTAGE": Packet.XL320_PESENT_VOLTAGE
}

class JsonFile(object):
	"""
	Simple class to handle json files.
	"""
	@staticmethod
	def readJson(fname):
		"""
		Reads a Json file
		in: file name
		out: length of file, dictionary
		"""
		try:
			with open(fname, 'r') as f:
				data = json.load(f)
			return data

		except IOError:
			raise Exception('Could not open {0!s} for reading'.format((fname)))

	@staticmethod
	def writeJson(fname, data):
		"""
		Writes a Json file
		"""
		try:
			with open(fname, 'w') as f:
				json.dump(data, f)

		except IOError:
			raise Exception('Could not open {0!s} for writing'.format((fname)))

def main():
	# filename = raw_input('File name >> ')
	# curr_id = raw_input('Enter current servo id >> ')
	filename = 'test.json'
	curr_id = 1
	port = 'a'

	ser = DummySerial(port)
	ser.open()

	jf = JsonFile()
	data = jf.readJson(filename)

	for key, val in data.items():
		print('> setting', key, val)

		reg = xl320_reg[key][0]
		reg_size = xl320_reg[key][1]

		if reg_size == 1:
			param = [val]
		else:
			param = le(val)

		pkt = Packet.makeWritePacket(curr_id, reg, param)
		ser.write(pkt)
		ser.read()

		# the servo id changed, so update it
		if key == 'XL320_ID':
			curr_id = val

if __name__ == '__main__':
	main()
