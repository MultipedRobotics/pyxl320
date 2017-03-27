#!/usr/bin/env python

from __future__ import print_function
from pyxl320 import listSerialPorts

"""
lists available serial ports
"""

err, ret = listSerialPorts()
print('Serial ports:')
map(print, ret)
