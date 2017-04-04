#!/usr/bin/env python3

import socket
import sys
import os
import urllib.request


dict={}				###save key-value
userpasswd={}		###save auth info: dict{username:passwd}
urlmap={}			###save url info: dict{username:[HTTP status, len(HTML)]}
name=[]				###save username
passwd=[]			###save passwd
authlist=[]			###save user authenticated

errorreport=0

### multi-process to handle socket connection
def server(host, port):
    host = host
    port = int(port)
    addr = (host, port)

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind(addr)
    except socket.error as e:
        print('failed create socket. error code:' + str(e[0]))
        sys.exit()

    serverSocket.listen(5)

    while True:
        connSocket, addr = serverSocket.accept()
        print('connect with ' + addr[0] + ':' + str(addr[1]))

        pid = os.fork()
        if pid > 0:
            connSocket.close()
        if pid == 0:
            #serverSocket.close()
            while True:
                data = connSocket.recv(1024)
                if not data or data =='':
                    print('recv nothing from client')
                    break
                message = data.decode()
                result = handleReq(message)
                ret = result
                if result=='null':
                    ret = '-1' + ' ' + errorreport
                elif result=='yes':
                    ret = '0'
                connSocket.send(ret.encode())
            print('close connetion')
            try:
                connSocket.close()
            except socket.error as e:
                print('connSocket close error')
    connSocket.close()
    serverSocket.close()

### set key:value
def setKeyValue(key, value):
	dict[key]=value
	return 'yes'

### get value of key
def getValue(key):
	if key in dict:
		return dict[key]
	else:
		global errorreport
		errorreport='getValue error'
		return 'null'

### authenticate username and passwd
def authentication(username, passwd):
	if username in userpasswd:
		if userpasswd[username]==passwd:
			if username not in authlist:
				authlist.append(username)
			return "yes"
	global errorreport
	errorreport='authenticate error'
	return "null"

### handle request from client detailedly
def handleReq(data):
	temp=[]
	temp = data.split();
	if temp[0].upper()=='SET':
		if len(temp)==3:
			return setKeyValue(temp[1],temp[2])
		else:
			print('setKeyValue error')
			global errorreport
			errorreport='setKeyValue error'
			return 'null'
	elif temp[0].upper()=='GET':
		if len(temp)==2:
			return getValue(temp[1])
		else:
			print('getValue error')
			global errorreport
			errorreport='getValue error'
			return 'null'
	elif temp[0].upper()=='AUTH':
		if len(temp)==3:
			return authentication(temp[1],temp[2])
		else:
			print('auth error')
			global errorreport
			errorreport='authenticate error'
			return 'null'
	elif temp[0].upper()=='URL':
		if len(temp)==3 and temp[1] in authlist:
			key=temp[1]
			value=temp[2]
			if key in urlmap:
				print(urlmap[key])
				return ' '.join(urlmap[key])
			else:
				url=urllib.request.urlopen(value)
				status=str(url.getcode())
				print('HTTP Status:',status)
				html=url.read()
				print(str(len(html)))
				print([status,len(html)])
				urlmap[key]=[status,str(len(html))]
				url.close()
				return ' '.join(urlmap[key])
		else:
			global errorreport
			errorreport='url error'
			return 'error'

### start to handle client request
def startFunc(argv):
	for i in range(1,len(argv)):
		if argv[i]=='--host':
			host = argv[i+1]
		else:
			if argv[i]=='--port':
				port = argv[i+1]
	if not 'host' in dir():
		host = 'localhost'
	if not 'port' in dir():
		port = '5678'
	server(host, port)

### read auth info from auth.conf
def readAuthConf():
	file = open('auth.conf')
	for line in file:
		print(line)
		line = line.split()
		if len(line)==2:
			name.append(line[0])
			passwd.append(line[1])
		else:
			continue;
	#print(name)
	#print(passwd)
	if len(name)!=len(passwd):
		print('auth.conf error')
		sys.exit()
		
	for i in range(0, len(name)):
		key = name[i]
		value = passwd[i]
		userpasswd[key]=value

### main function
if __name__ == '__main__':
	readAuthConf()
	startFunc(sys.argv)
