import socket
import sys
import os
import urllib.request

dict={}
userpasswd={}
urlmap={}           #url信息: dict{username:[HTTP status, len(HTML)]}
name=[]				#用户名
passwd=[]			#密码
authlist=[]			#用户验证信息

errorreport=0

# 多进程程处理socket连接
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

#set key value
def setKeyValue(key, value):
	dict[key]=value
	return 'yes'

#get key
def getValue(key):
	if key in dict:
		return dict[key]
	else:
		global errorreport
		errorreport='getValue error'
		return 'null'

### 验证用户名和密码
def authentication(username, passwd):
	if username in userpasswd:
		if userpasswd[username]==passwd:
			if username not in authlist:
				authlist.append(username)
			return "yes"
	global errorreport
	errorreport='authenticate error'
	return "null"

def handleReq(data):
	temp=[]
	temp = data.split();
	global errorreport
	if temp[0].upper()=='SET':
		if len(temp)==3:
			return setKeyValue(temp[1],temp[2])
		else:
			print('setKeyValue error')
			errorreport='setKeyValue error'
			return 'null'
	elif temp[0].upper()=='GET':
		if len(temp)==2:
			return getValue(temp[1])
		else:
			print('getValue error')
			errorreport='getValue error'
			return 'null'
	elif temp[0].upper()=='AUTH':
		if len(temp)==3:
			return authentication(temp[1],temp[2])
		else:
			print('auth error')
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
			errorreport='url error'
			return 'null'
	else:
		errorreport='input error'
		return 'null'


#开始处理客户端的请求
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

#从auth.conf文件中读取用户的验证信息
def readAuthConf():
	file = open('auth.conf')
	for line in file:
		line = line.split()
		if len(line)==2:
			name.append(line[0])
			passwd.append(line[1])
		else:
			continue;
	if len(name)!=len(passwd):
		print('auth.conf error')
		sys.exit()
		
	for i in range(0, len(name)):
		key = name[i]
		value = passwd[i]
		userpasswd[key]=value

if __name__ == '__main__':
	readAuthConf()
	startFunc(sys.argv)
