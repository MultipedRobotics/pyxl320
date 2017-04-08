#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from setuptools import setup
from pyxl320 import __version__ as VERSION
import os
from setuptools.command.test import test as TestCommand
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
	def is_pure(self):
		return False


class PublishCommand(TestCommand):
	def run_tests(self):
		print('Publishing to PyPi ...')
		os.system("python3 setup.py sdist")
		# os.system("python2 setup.py sdist")
		os.system("python2 setup.py bdist_wheel")
		os.system("python3 setup.py bdist_wheel")
		os.system("twine upload dist/pyxl320-{}*".format(VERSION))


setup(
	author='Kevin Walchko',
	author_email='kevin.walchko@outlook.com',
	name='pyxl320',
	version=VERSION,
	description='A library to control dynamixel XL-320 servos with python',
	long_description=open('README.rst').read(),
	url='http://github.com/walchko/pyxl320',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.6',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Libraries :: Application Frameworks'
	],
	license='MIT',
	keywords='dynamixel xl320 xl-320 servo actuator library robotics spider',
	packages=['pyxl320'],
	install_requires=['pyserial', 'simplejson'],
	cmdclass={
		'publish': PublishCommand
	},
	scripts=[
		'bin/set_id.py',
		'bin/servo_ping.py',
		'bin/set_angle.py',
		'bin/set_baud_rate.py',
		'bin/servo_reboot.py',
		'bin/servo_reset.py'
	]
)
