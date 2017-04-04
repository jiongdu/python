#!/usr/bin/env python3

import socket              # use socket.*
#from socket import *      # use module directly
import sys
import signal

### handle signal
def signal_handle(a,b):
	print('signal handle exec')
	clientSocket.close()
	sys.exit()

signal.signal(signal.SIGTERM, signal_handle)

signal.signal(signal.SIGINT, signal_handle)

clientSocket=0

### handle client input and interact with server
def connect(argv):    
	for i in range(1,len(argv)):
		##pirnt(args[i])
		if argv[i]=='--host':
			host = argv[i+1]
		else:
			if argv[i]=='--port':
				port = argv[i+1]
	if not 'host' in dir():
		host = 'localhost'
	if not 'port' in dir():
		port = 5678
	addr=(host, int(port))
	try:
		global clientSocket
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print('failed create socket. error code:' + str(e[0]))
		sys.exit()

	clientSocket.connect(addr)
	
	while True:
		print('connect server successfully!')
		message = input('Input your choices:')
		if not message:
			continue
		###TODO: if input error, show_usage()
		clientSocket.send(message.encode())
		data = clientSocket.recv(1024)
		print(data.decode())

	clientSocket.close()

### main function
if __name__ == '__main__':
	connect(sys.argv)
