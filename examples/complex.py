#!/usr/bin/env python

from __future__ import division, print_function
from pyxl320 import ServoSerial, Packet, xl320
from pyxl320 import DummySerial
from time import sleep
import sys

"""
This example rotates the servo back and forth while cycling through the different
colors of the LED.

It assumes default setting on the servo.
"""


# modify these for your servo
ID = 1
port = '/dev/tty.usbserial-A5004Flb'
sleep_time = 0.1
speed = 0.5  # 50% speed

# serial = ServoSerial(port)
serial = DummySerial(port)  # use this for simulation
serial.open()


pkt = Packet.makeServoSpeedPacket(ID, speed)  # set servo speed
serial.sendPkt(pkt)

try:
	led_color = 0
	while True:
		led_color = led_color % 7 + 1
		pkt = Packet.makeLEDPacket(ID, led_color)
		serial.sendPkt(pkt)
		for angle in range(0, 300, 10):
			pkt = Packet.makeServoPacket(ID, angle)
			serial.sendPkt(pkt)
			sleep(sleep_time)

		led_color = led_color % 7 + 1
		pkt = Packet.makeLEDPacket(ID, led_color)
		serial.sendPkt(pkt)
		for angle in range(300, 0, -10):
			pkt = Packet.makeServoPacket(ID, angle)
			serial.sendPkt(pkt)
			sleep(sleep_time)
except:
	e = sys.exc_info()[0]
	print(e)
	sleep(0.25)
	pkt = Packet.makeLEDPacket(ID, xl320.XL320_LED_OFF)
	serial.sendPkt(pkt)
	pkt = Packet.makeServoPacket(ID, 150.0)  # move servo to center
	serial.sendPkt(pkt)  # send packet to servo
	serial.close()
