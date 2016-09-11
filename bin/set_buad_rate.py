#!/usr/bin/env python
# ----------------------------
# Simple tool to change the id number of a servo
#

from __future__ import print_function, division
from pyxl320 import ServoSerial, Packet, xl320
from pyxl320 import DummySerial
import argparse




# def makeInterActive():
# 	port = raw_input('Enter serial port >> ')
# 	curr_id = raw_input('Enter current id >> ')
# 	new_id = raw_input('Enter new id >> ')
# 	return port, curr_id, new_id


def sendCmd(serial, pkt):
	wait_for_return = True
	while wait_for_return:
		serial.write(pkt)  # send packet to servo
		ans = serial.read()  # get return status packet
		if ans:
			wait_for_return = False
			err_num, err_str = Packet.getErrorString(ans)
			# print(num, ret)
			if err_num:
				print('Error[{}]: {}'.format(err_num, err_str))
			else:
				print('step packet {}'.format(ans))
		else:
			print('>> retry <<')

def handleArgs():
	parser = argparse.ArgumentParser(description='set servo id')
	parser.add_argument('-i', '--interactive', help='input via commandline', action='store_true')
	# parser.add_argument('-c', '--camera', help='set opencv camera number, ex. -c 1', type=int, default=0)
	# parser.add_argument('-t', '--type', help='set type of camera: cv or pi, ex. -t pi', default='cv')
	# parser.add_argument('-s', '--set', help='set id', nargs=2, type=int, default=(320, 240))
	parser.add_argument('-s', '--set', help='set id', type=int, default=1)
	parser.add_argument('-c', '--current', help='current id', type=int, default=1)
	parser.add_argument('-p', '--port', help='serial port', type=str, default='tty.usbserial-A5004Flb')

	args = vars(parser.parse_args())
	return args


def main():
	# args = handleArgs()

	# if args['interactive']:
	# 	port, curr_id, new_id = makeInterActive()
	# else:
	# 	port = args['port']
	# 	curr_id = args['current']
	# 	new_id = args['set']

	ID = 1
	port = '/dev/tty.usbserial-A5004Flb'
	# 0: 9600, 1:57600, 2:115200, 3:1Mbps
	rate = 2

	ser = ServoSerial(port, 57600)
	ser.open()

	pkt = Packet.makeBaudRatePacket(ID, rate)
	sendCmd(ser, pkt)

	pkt = Packet.makeRebootPacket(ID)
	sendCmd(ser, pkt)

if __name__ == '__main__':
	main()
