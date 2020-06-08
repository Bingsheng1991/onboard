#!/usr/bin/python
# -*- coding: UTF-8 -*-

from smbus2 import SMBus, i2c_msg
import sys
import time
import socket

I2C_CHANNEL = 4
ROB_ADDR = 0x1F
ACTUATORS_SIZE = (19 + 1)  # Data + checksum.
SENSORS_SIZE = (46 + 1)  # Data + checksum.

def update_robot_sensors_and_actuators():
	global sensors_data
	global actuators_data
	try:
		write = i2c_msg.write(ROB_ADDR, actuators_data)
		read = i2c_msg.read(ROB_ADDR, SENSORS_SIZE)
		bus.i2c_rdwr(write, read)
		sensors_data = list(read)
	except:
		sys.exit(1)


actuators_data = bytearray([0] * ACTUATORS_SIZE)
sensors_data = bytearray([0] * SENSORS_SIZE)
prox = [0 for x in range(8)]
prox_amb = [0 for x in range(8)]
mic = [0 for x in range(4)]
mot_steps = [0 for x in range(2)]
try:
	bus = SMBus(I2C_CHANNEL)
except:
	sys.exit(1)


counter = 0
actuators_state = 0

while 1:

	start = time.time()

	counter += 1
	if(counter == 20):
		counter = 0
		actuators_data[0] = 0		# Left speed: 512
		actuators_data[1] = 0
		actuators_data[2] = 0		# Right speed: -512
		actuators_data[3] = 0



	checksum = 0
	for i in range(ACTUATORS_SIZE-1):
		checksum ^= actuators_data[i]
	actuators_data[ACTUATORS_SIZE-1] = checksum

	update_robot_sensors_and_actuators()

	#if len(sensors_data) < 0:
	#	sys.exit(1)



	# Communication frequency @ 20 Hz.
	time_diff = time.time() - start
	if time_diff < 0.050:
		time.sleep(0.050 - time_diff)

