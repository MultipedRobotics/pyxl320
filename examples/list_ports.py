#!/usr/bin/env python

from __future__ import print_function
from pyxl320 import ServoSerial

"""
lists available serial ports
"""

err, ret = ServoSerial.listSerialPorts()
print('Serial ports:')
map(print, ret)
