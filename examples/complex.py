#!/usr/bin/env python

from __future__ import division, print_function
from pyxl320 import ServoSerial
from pyxl320 import Packet
from pyxl320 import xl320
from pyxl320 import DummySerial
from time import sleep
# import sys

"""
This example rotates the servo back and forth while cycling through the different
colors of the LED.

It assumes default setting on the servo.
"""

Error = {
	0: 'NO_ERROR',
	1: 'ERROR_OVERLOAD',
	2: 'ERROR_OVER_HEATING',
	4: 'ERROR_INPUT_VALTAGE',
	99: 'NOT_STATUS_PACKET'
}


def word(l, h):
	return (h << 8) + l


def status_error(pkt):
	if pkt[7] == xl320.XL320_STATUS:
		if pkt[8] == 0:
			return 0
		else:
			return pkt[8]
	else:
		# print('pkt:', pkt)
		return 99


def run(ID, serial, maxs, mins, delta):
	sleep_time = 0.2
	led_color = 0
	pkt = Packet.makeLEDPacket(ID, xl320.XL320_LED_OFF)
	serial.sendPkt(pkt)
	pkt = Packet.makeServoPacket(ID, 150)
	serial.sendPkt(pkt)
	sleep(1)
	for angle in range(mins, maxs, delta):
		led_color = led_color % 7 + 1
		pkt = Packet.makeLEDPacket(ID, led_color)
		serial.sendPkt(pkt)
		pkt = Packet.makeServoPacket(ID, angle)
		ret = serial.sendPkt(pkt)
		# print('ret:', ret)
		for p in ret:
			err = status_error(p)
			if not err:
				pass
			elif err == 99:
				print('echo?', p)
				# pass  # this is a echo
			else:
				print('<<< ERROR:', Error[err], '>>>')

		sleep(sleep_time)
		# ret = serial.read()
		# print('ret:', ret)

	pkt = Packet.makeLEDPacket(ID, xl320.XL320_LED_OFF)
	serial.sendPkt(pkt)
	pkt = Packet.makeServoPacket(ID, 150)
	serial.sendPkt(pkt)
	sleep(1)


# modify these for your system
ID = xl320.XL320_BROADCAST_ADDR  # I seem to get better performance on braodcast
# port = '/dev/tty.usbserial-A5004Flb'
# port = '/dev/tty.usbserial-A700h2xE'
# port = '/dev/tty.usbserial-A5004Fnd'
# port = '/dev/tty.usbserial-A5004Flb'
port = '/dev/tty.usbserial-AL034G2K'
speed = 0.5  # 50% speed

if port is 'dummy':
	serial = DummySerial(port)  # use this for simulation
else:
	serial = ServoSerial(port)
serial.open()

pkt = Packet.makeServoSpeedPacket(ID, speed)  # set servo speed
serial.sendPkt(pkt)

try:
	while True:
		run(ID, serial, 300, 0, 10)
		print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
		run(ID, serial, 0, 300, -10)
		print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
		sleep(2)

except KeyboardInterrupt:
	# e = sys.exc_info()[0]
	# print(e)
	pkt = Packet.makeLEDPacket(ID, xl320.XL320_LED_OFF)
	serial.sendPkt(pkt)
	pkt = Packet.makeServoPacket(ID, 150.0)  # move servo to center
	serial.sendPkt(pkt)  # send packet to servo
	serial.close()
	sleep(0.25)
