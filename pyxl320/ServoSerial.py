#!/usr/bin/env python

from __future__ import division, print_function
import serial
import Packet


class DummySerial(object):
	"""
	A dummy interface to test with when not hooked up to real hardware. It does
	a decent job of mimicing the real thing.
	"""
	def __init__(self, port):
		self.port = port

	def open(self):
		pass

	def read(self):
		return [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]

	def write(self, data):
		print('serial:', data)
		return len(data)

	def close(self):
		pass


class ServoSerial(object):
	"""
	A wrapper around pyserial to work with Dynamixel servos' half duplex
	interface. This requires extra hardware added to your normal full duplex
	serial port. Also, this uses the  RTS pin to toggle between Tx and Rx.

	All data that goes into this class via write() or returns from it via read()
	is a simple array of bytes (e.g., [1,34,234,1,0,24,67]). Internally, the class
	transforms those into a binary stream.
	"""
	DD_WRITE = False     # data direction set to write
	DD_READ = True       # data direction set to read
	SLEEP_TIME = 0.00001 # sleep time between read/write

	def __init__(self, port):
		self.serial = serial.Serial()
		self.serial.baudrate = 1000000
		self.serial.port = port
		self.serial.timeout = 0.0001  # time out between read/write

	def __del__(self):
		if self.serial.isOpen():
			self.serial.close()

	@staticmethod
	def listSerialPorts():
		"""
		http://pyserial.readthedocs.io/en/latest/shortintro.html
		"""
		ans = serial.tools.list_ports
		return ans

	def open(self):
		self.serial.open()
		self.serial.setRTS(self.DD_WRITE)
		serial.time.sleep(self.SLEEP_TIME)
		if self.serial.isOpen():
			print('Opened port:', self.serial.name)
			print('baudrate:', self.serial.baudrate)
			print(self.serial.get_settings())
		else:
			raise Exception('Could not open {}'.format(self.serial.port))

	@staticmethod
	def decode(buff):
		pp = list(map(ord, buff))
		if 0 == len(pp) == 1:
			pp = []
		return pp

	def read(self):
		self.serial.flushInput()
		self.serial.setRTS(self.DD_READ)
		serial.time.sleep(self.SLEEP_TIME)
		# print('in_waiting:', self.serial.inWaiting())
		data = self.serial.read(256)
		return self.decode(data)

	def write(self, data):
		data = bytearray(data)
		data = bytes(data)
		self.serial.flushOutput()
		self.serial.setRTS(self.DD_WRITE)
		serial.time.sleep(self.SLEEP_TIME)
		num = self.serial.write(data)
		# print('out_waiting:', self.serial.out_waiting)
		# self.serial.flushOutput()
		return num

	def close(self):
		self.serial.close()
