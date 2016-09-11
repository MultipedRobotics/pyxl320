#!/usr/bin/env python

from __future__ import division, print_function
import serial as PySerial
import Packet
import commands


class DummySerial(object):
	"""
	A dummy interface to test with when not hooked up to real hardware. It does
	a decent job of mimicing the real thing.
	"""
	def __init__(self, port, printAll=False):
		self.port = port
		self.printAll = printAll


	@staticmethod
	def listSerialPorts():
		return ServoSerial.listSerialPorts()

	def open(self):
		pass

	def sendPkt(self, pkt):
		pass

	def read(self):
		return [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]

	def write(self, data):
		# if self.printAll:
		print('serial write >>', data)
		return len(data)

	def close(self):
		pass

	def flushInput(self):
		pass


class ServoSerial(object):
	"""
	A wrapper around pyserial to work with Dynamixel servos' half duplex
	interface. This requires extra hardware added to your normal full duplex
	serial port. Also, this uses the  RTS pin to toggle between Tx and Rx.

	All data that goes into this class via write() or returns from it via read()
	is a simple array of bytes (e.g., [1,34,234,1,0,24,67]). Internally, the class
	transforms those into a binary stream.

	This class also uses Packet to find and verify what is returned form read()
	is a valid packet.
	"""
	DD_WRITE = False      # data direction set to write
	DD_READ = True        # data direction set to read
	SLEEP_TIME = 0.005  # sleep time between read/write

	def __init__(self, port, baud_rate=1000000):
		self.serial = PySerial.Serial()
		self.serial.baudrate = baud_rate
		self.serial.port = port
		# the default time delay on the servo is 0.5 msec before it returns a status pkt
		self.serial.timeout = 0.001  # time out between read/write

	def __del__(self):
		self.close()

	@staticmethod
	def listSerialPorts():
		"""
		http://pyserial.readthedocs.io/en/latest/shortintro.html
		"""
		cmd = 'python -m serial.tools.list_ports'
		err, ret = commands.getstatusoutput(cmd)
		if not err:
			r = ret.split('\n')
			ret = []
			for line in r:
				if line.find('/dev/') >= 0:
					line = line.replace(' ', '')
					ret.append(line)
		return err, ret

	def open(self):
		if self.serial.isOpen():
			raise Exception('SeroSerial::open() ... Oops, port is already open')
		self.serial.open()
		self.serial.setRTS(self.DD_WRITE)
		PySerial.time.sleep(self.SLEEP_TIME)
		if self.serial.isOpen():
			print('Opened {} @ {}'.format(self.serial.name, self.serial.baudrate))
			print(self.serial.get_settings())
		else:
			raise Exception('Could not open {}'.format(self.serial.port))

	@staticmethod
	def decode(buff):
		pp = list(map(ord, buff))
		if 0 == len(pp) == 1:
			pp = []
		return pp

	# @staticmethod
	# def findPkt(pkt):
	# 	"""
	# 	Search through a string of binary for a valid xl320 package.
	#
	# 	in: buffer to search through
	# 	out: a list of valid data packet
	# 	"""
	# 	ret = []
	# 	while len(pkt)-11 >= 0:
	# 		if pkt[0:4] != [0xFF, 0xFF, 0xFD, 0x00]:
	# 			pkt.pop(0)  # get rid of the first index
	# 			# print('pop')
	# 			continue
	# 		# pcrc = pkt[-2:]  # get crc from packet
	# 		# crc = crc16(pkt[:-2])  # calculate crc from packet
	# 		length = (pkt[6] << 8) + pkt[5]
	# 		# print('length', length)
	# 		crc_pos = 5 + length
	# 		# pkt_crc = [pkt[crc_pos], pkt[crc_pos+1]]
	# 		pkt_crc = pkt[crc_pos:crc_pos + 2]
	# 		# print(pkt_crc)
	# 		crc = le(crc16(pkt[:crc_pos]))
	# 		# print(crc)
	# 		# print('pkt {}'.format(pkt[:crc_pos]))
	# 		if pkt_crc == crc:
	# 			pkt_end = crc_pos+2
	# 			ret.append(pkt[:pkt_end])
	# 			del pkt[:pkt_end]
	# 		else:
	# 			del pkt[:11]
	# 	return ret

	def read(self):
		# self.serial.flushInput()
		self.serial.setRTS(self.DD_READ)
		PySerial.time.sleep(self.SLEEP_TIME)
		# print('in_waiting:', self.serial.inWaiting())
		data = self.serial.read(256)
		data = self.decode(data)
		# return data
		ret = []
		d = Packet.findPkt(data)
		if len(d) > 0:
			ret = d[0]
		return ret  # what do i do if i find more?

	def write(self, data):
		# print('hello write')
		self.serial.setRTS(self.DD_WRITE)
		# prep data array for transmition
		data = bytearray(data)
		data = bytes(data)

		# self.serial.flushOutput()
		# self.serial.setRTS(self.DD_WRITE)
		PySerial.time.sleep(self.SLEEP_TIME)
		num = self.serial.write(data)
		print('wrote {} of len(pkt) == {}'.format(num, len(data)))
		# print('out_waiting:', self.serial.out_waiting)
		self.serial.flushOutput()
		# print('flush')
		return num

	def sendPkt(self, pkt):
		"""
		Sends a packet and waits for a return. If no return is given, then it
		resends the packet. If an error occurs, it also resends the packet.
		"""
		wait_for_return = True
		while wait_for_return:
			# print('going write')
			self.write(pkt)  # send packet to servo
			ans = self.read()  # get return status packet
			if ans:
				wait_for_return = False
				err_num, err_str = Packet.getErrorString(ans)
				if err_num:
					print('Error[{}]: {}'.format(err_num, err_str))
				else:
					print('packet {}'.format(ans))
			else:
				print('>> retry <<')


	def close(self):
		if self.serial.isOpen():
			self.serial.close()

	def flushInput(self):
		self.serial.flushInput()
