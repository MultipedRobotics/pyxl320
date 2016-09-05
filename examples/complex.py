#!/usr/bin/env python

import pyxl320
from pyxl320 import ServoSerial, Packet, utils, xl320
from pyxl320 import DummySerial
from time import sleep

# modify these for your servo
ID = 1
port = '/dev/tty.usbserial-A5004Flb'
sleep_time = 0.01

serial = ServoSerial(port)  # use this if you want to talk to real servos
# serial = DummySerial(port)  # tell it what port you want to use
serial.open()

pkt = Packet.makeServoSpeed(ID, 75)  # set speed to 75%

try:
	led_color = 0
	while True:
		led_color = led_color % 7 + 1
		pkt = Packet.makeLEDPacket(ID, led_color)
		serial.write(pkt)
		for angle in range(0, 300):
			pkt = Packet.makeServoPacket(ID, angle)  # move servo 1 to 158.6 degrees
			serial.write(pkt)  # send packet to servo
			ans = serial.read()  # get return status packet
			print('step {} packet {}'.format(angle, ans))
			sleep(sleep_time)

		led_color = led_color % 7 + 1
		pkt = Packet.makeLEDPacket(ID, led_color)
		serial.write(pkt)
		for angle in range(300, 0, -1):
			pkt = Packet.makeServoPacket(ID, angle)  # move servo 1 to 158.6 degrees
			serial.write(pkt)  # send packet to servo
			ans = serial.read()  # get return status packet
			sleep(sleep_time)
except:
	sleep(0.25)
	pkt = Packet.makeLEDPacket(ID, xl320.XL320_LED_OFF)
	serial.write(pkt)
	pkt = Packet.makeServoPacket(ID, 150.0)  # move servo 1 to 158.6 degrees
	serial.write(pkt)  # send packet to servo
	serial.close()
