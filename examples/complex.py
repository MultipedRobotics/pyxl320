#!/usr/bin/env python

from __future__ import division, print_function
import pyxl320
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
ID = 10
port = '/dev/tty.usbserial-A5004Flb'
sleep_time = 0.1
speed = 0.5  # 50% speed

# err, ret = ServoSerial.listSerialPorts()
# print('Serial ports:')
# map(print, ret)
serial = ServoSerial(port)
# serial = ServoSerial(port, 115200)  # use this if you want to talk to real servos
# serial = DummySerial(port)  # use this for simulation
serial.open()


# def sendCmd(angle):
# 	wait_for_return = True
# 	while wait_for_return:
# 		pkt = Packet.makeServoPacket(ID, angle)  # move servo
# 		serial.write(pkt)  # send packet to servo
# 		ans = serial.read()  # get return status packet
# 		if ans:
# 			wait_for_return = False
# 			err_num, err_str = Packet.getErrorString(ans)
# 			if err_num:
# 				print('Error[{}]: {}'.format(err_num, err_str))
# 			else:
# 				print('step {} packet {}'.format(angle, ans))
# 		else:
# 			print('>> retry <<')
# 			# wait_for_return = False


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
		serial.write(pkt)
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
