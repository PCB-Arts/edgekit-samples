#!/usr/bin/env python3

import os
import sys

import os
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, '../GPIO'))  # Add path to GPIO lib

from gpio import *

MODULE = "Nano"
# MODULE = "NX"

if MODULE == "Nano":
	SERIAL_OUTPUT_SELCTOR = "38"
	SERIAL_120_TERMINATION = "492"
	SERIAL_SLEW_LIMIT = "495"
	SERIAL_MODE_1 = "493"
	SERIAL_MODE_0 = "494"
elif MODULE == "NX":
	SERIAL_OUTPUT_SELCTOR = "393"
	SERIAL_120_TERMINATION = "228"
	SERIAL_SLEW_LIMIT = "231"
	SERIAL_MODE_1 = "229"
	SERIAL_MODE_0 = "230"
else:
	raise NotImplementedError("Unknown Module: %s", MODULE)


def export_and_output(gpio):
	""" Export a gpio and define it as output """
	export(gpio)
	set_output(gpio)


def export_pins():
	""" Export all gpios and define them as output """
	export_and_output(SERIAL_OUTPUT_SELCTOR)
	export_and_output(SERIAL_120_TERMINATION)
	export_and_output(SERIAL_SLEW_LIMIT)
	export_and_output(SERIAL_MODE_1)
	export_and_output(SERIAL_MODE_0)


if __name__ == "__main__":
	print("""
	Select one of the following modes:
		1: RS232
		2: RS485
		3: RS422
		4: loopback
	""")

	mode = input("Mode: ")

	if mode in ("1", "RS232"):
		print("Setting mode to RS232")
		os.popen("stty -F /dev/ttyTHS1 crtscts").read()
		export_pins()
		set_high(SERIAL_OUTPUT_SELCTOR)  # Switch serial output from 40pin header to D-Sub
		set_high(SERIAL_MODE_0)
		set_low(SERIAL_MODE_1)
	elif mode in ("2", "RS485"):
		print("Setting mode to RS485")
		os.popen("stty -F /dev/ttyTHS1 -crtscts").read()
		export_pins()
		set_high(SERIAL_OUTPUT_SELCTOR)  # Switch serial output from 40pin header to D-Sub
		set_low(SERIAL_MODE_0)
		set_high(SERIAL_MODE_1)
	elif mode in ("3", "RS422"):
		print("Setting mode to RS422")
		os.popen("stty -F /dev/ttyTHS1 -crtscts").read()
		export_pins()
		set_high(SERIAL_OUTPUT_SELCTOR)  # Switch serial output from 40pin header to D-Sub
		set_high(SERIAL_MODE_0)
		set_high(SERIAL_MODE_1)
	elif mode in ("4", "loopback"):
		print("Setting mode to loopback")
		os.popen("stty -F /dev/ttyTHS1 -crtscts").read()
		export_pins()
		set_high(SERIAL_OUTPUT_SELCTOR)  # Switch serial output from 40pin header to D-Sub
		set_low(SERIAL_MODE_0)
		set_low(SERIAL_MODE_1)
	else:
		print("Got unknown input, exiting now")
		exit(1)

	set_low(SERIAL_120_TERMINATION)
	set_low(SERIAL_SLEW_LIMIT)
	print("Configured serial interface /dev/ttyTHS1")

	# to send some test-data, uncomment following code-block:
	"""
	with open("/dev/ttyTHS1", "w") as f:
		f.write("test")
	"""

	print("done")
