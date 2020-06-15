#!/usr/bin/python
# -*- coding: UTF-8 -*-

from smbus2 import SMBus, i2c_msg
import sys
import time

I2C_CHANNEL = 4
ROB_ADDR = 0x1F
ACTUATORS_SIZE = (19 + 1)  # Data + checksum.
SENSORS_SIZE = (46 + 1)  # Data + checksum.
movement = [0,0,0,0]

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

##############################socket client###########################################
import socket# 客户端 发送一个数据，再接收一个数据
Host = '192.168.1.123' #server addr
Port = 8888 #e-puck id
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
client.connect((Host,Port)) #connet to server
client.send("0".encode('utf8'))

actuators_data = bytearray([0] * ACTUATORS_SIZE)
sensors_data = bytearray([0] * SENSORS_SIZE)
prox = [0 for x in range(8)]
prox_amb = [0 for x in range(8)]
mic = [0 for x in range(4)]
mot_steps = [0 for x in range(2)]
counter = 0
actuators_state = 0

try:
	bus = SMBus(I2C_CHANNEL)
except:
	sys.exit(1)

while True:
	# data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
	# print('recv:',data) #输出我接收的信息
	# print('##############################################################')
	# try:
	get_data = client.send(str.encode("epuck"))
	data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
	data_decode = str(data, encoding="utf-8")
	if data_decode == 'spin_right':
		movement = bytearray([0x20, 0x00, 0xE0, 0xFF])
	elif data_decode == 'spin_left':
		movement = bytearray([0xE0, 0xFF, 0x20, 0x00])
	elif data_decode == 'move_forward':
		movement = bytearray([0x20, 0x00,0x20, 0x00])
	elif data_decode == 'stop':
		movement = bytearray([0, 0, 0, 0])

	print('movement:',data_decode) #输出我接收的信息
#	time.sleep(0.5)
	# except:
	# 	client.close()
	# 	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
	# 	client.connect((Host,Port)) #connet to server
	# 	client.send("E-Pcuk 4786 reconnect".encode('utf8'))

######################################################################################

	# start = time.time()

#	counter = 0
	actuators_data[0] = movement[0]		# Left speed: 512
	actuators_data[1] = movement[1]
	actuators_data[2] = movement[2]		# Right speed: -512
	actuators_data[3] = movement[3]


	checksum = 0
	for i in range(ACTUATORS_SIZE-1):
		checksum ^= actuators_data[i]
	actuators_data[ACTUATORS_SIZE-1] = checksum

	update_robot_sensors_and_actuators()
	time.sleep(0.1)
client.close() #关闭这个链接
