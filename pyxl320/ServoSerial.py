#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division, print_function
import serial as PySerial
import Packet
import commands

"""
Serial interfaces (real and test) for communications with XL-320 servos.
"""

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
# 		print('serial write >>', pkt)
		return 0, None

	def readPkts(self, how_much=128):
		return [[0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C], [0xFF, 0xFF, 0xFD, 0x00, 0x03, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]]

	def read(self, how_much=128):
		return [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]

	def write(self, data):
		# if self.printAll:
# 		print('serial write >>', data)
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
	SLEEP_TIME = 0.005    # sleep time between read/write

	def __init__(self, port, baud_rate=1000000):
		"""
		Constructor: sets up the serial port
		"""
		self.serial = PySerial.Serial()
		self.serial.baudrate = baud_rate
		self.serial.port = port
		# the default time delay on the servo is 0.5 msec before it returns a status pkt
		self.serial.timeout = 0.001  # time out waiting for blocking read()

	def __del__(self):
		"""
		Destructor: closes the serial port
		"""
		self.close()

	@staticmethod
	def listSerialPorts():
		"""
		http://pyserial.readthedocs.io/en/latest/shortintro.html

		This calls the command line tool from pyserial to list the available
		serial ports.
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
		"""
		Transforms the raw buffer data read in into a list of bytes
		"""
		pp = list(map(ord, buff))
		if 0 == len(pp) == 1:
			pp = []
		return pp

	def read(self, how_much=128):  # FIXME: 128 might be too much ... what is largest?
		"""
		This toggles the RTS pin and reads in data. It also converts the buffer
		back into a list of bytes and searches through the list to find valid
		packets of info.
		"""
		self.serial.setRTS(self.DD_READ)
		PySerial.time.sleep(self.SLEEP_TIME)
		data = self.serial.read(how_much)
		data = self.decode(data)
		# return data
		ret = []
		d = Packet.findPkt(data)
		if len(d) > 0:  # FIXME: need a better way
			ret = d[0]  # should i take the last one ... most recent?
		return ret  # what do i do if i find more?

	def readPkts(self, how_much=128):  # FIXME: 128 might be too much ... what is largest?
		"""
		This toggles the RTS pin and reads in data. It also converts the buffer
		back into a list of bytes and searches through the list to find valid
		packets of info.
		"""
		self.serial.setRTS(self.DD_READ)
		PySerial.time.sleep(self.SLEEP_TIME)
		data = self.serial.read(how_much)
		data = self.decode(data)
		# return data
		ret = Packet.findPkt(data)
		return ret

	def write(self, pkt):
		"""
		This is a simple serial write command. It toggles the RTS pin and formats
		all of the data into bytes before it writes.
		"""
		self.serial.setRTS(self.DD_WRITE)
		# prep data array for transmition
		pkt = bytearray(pkt)
		pkt = bytes(pkt)

		PySerial.time.sleep(self.SLEEP_TIME)
		num = self.serial.write(pkt)
		# print('wrote {} of len(pkt) == {}'.format(num, len(data)))
		self.serial.flushOutput()  # flush anything in the buffer
		return num

	def sendPkt(self, pkt):
		"""
		Sends a packet and waits for a return. If no return is given, then it
		resends the packet. If an error occurs, it also resends the packet.

		in: pkt - command packet to send to servo
		out:
			err_num - 0 if good, >0 if error
			err_str - None if good, otherwise a string
		"""
		err_num = 0
		err_str = None
		wait_for_return = True
		while wait_for_return:
			# print('going write')
			self.write(pkt)  # send packet to servo
			ans = self.read()  # get return status packet
			if ans:
				wait_for_return = False
				err_num, err_str = Packet.getErrorString(ans)
				if err_num:  # something went wrong, exit function
					print('Error[{}]: {}'.format(err_num, err_str))
					wait_for_return = True
				else:
					print('packet {}'.format(ans))
			else:
				print('>> retry <<')
		return err_num, err_str

	def close(self):
		"""
		If the serial port is open, it closes it.
		"""
		if self.serial.isOpen():
			self.serial.close()

	def flushInput(self):
		"""
		Flush the input.
		"""
		self.serial.flushInput()
