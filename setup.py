#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup
from pyxl320 import __version__ as VERSION
import os
from setuptools.command.test import test as TestCommand


# http://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-setuptools-test-command/
class NoseTestCommand(TestCommand):
	def run_tests(self):
		print('Running nose tests ...')
		os.system('nosetests -v test/test.py')


class PublishCommand(TestCommand):
	def run_tests(self):
		print('Publishing to PyPi ...')
		os.system("python setup.py sdist")
		os.system("twine upload dist/pyxl320-{}.tar.gz".format(VERSION))


class GitTagCommand(TestCommand):
	def run_tests(self):
		print('Creating a tag for version {} on git ...'.format(VERSION))
		os.system("git tag -a {} -m 'version {}'".format(VERSION, VERSION))
		os.system("git push --tags")


class CleanCommand(TestCommand):
	def run_tests(self):
		print('Cleanning up ...')
		os.system('rm -fr pyxl320.egg-info dist')


setup(
	author='Kevin Walchko',
	author_email='kevin.walchko@outlook.com',
	name='pyxl320',
	version=VERSION,
	description='A library to control dynamixel XL-320 servos with python',
	long_description=open('README.rst').read(),
	url='http://github.com/walchko',
	classifiers=['Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Libraries :: Application Frameworks'
	],
	license='MIT',
	keywords='dynamixel xl320 xl-320 servo actuator library robotics spider',
	packages=['pyxl320'],
	install_requires=['pyserial', 'simplejson'],
	setup_requires=[
		'nose',
		# 'coverage',
		# 'mock'
	],
	cmdclass={
		'test': NoseTestCommand,
		'publish': PublishCommand,
		'tag': GitTagCommand,
		'clean': CleanCommand
	},
	scripts=[
		'bin/set_id.py'
	],
	# entry_points={
	# 	'console_scripts': [
	# 		# 'pyarchey=pyarchey.pyarchey:main',
	# 	],
	# },
)
