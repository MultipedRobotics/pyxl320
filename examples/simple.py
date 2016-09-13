#!/usr/bin/env python

# from pyxl320 import ServoSerial
from pyxl320 import Packet
from pyxl320 import DummySerial

ID = 1
port = '/dev/tty.usbserial-A5004Flb'
angle = 158.6

# serial = ServoSerial(port)  # use this if you want to talk to real servos
serial = DummySerial(port)  # use this for simulation
serial.open()

pkt = Packet.makeServoPacket(ID, angle)  # move servo 1 to 158.6 degrees
err_no, err_str = serial.sendPkt(pkt)  # send packet to servo
if err_no:
	print('Oops ... something went wrong!')
