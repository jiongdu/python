### 基于Python3,实现了一个类似redis的Key–Value存储。

#### 服务端    
##### python3 server.py --host [ADDRESS] --port [PORT]    
1. 监听地址由--host 和 --port 指定，默认为 localhost:5678。
2. SET key value 如果key已经持有其他值,SET就覆写旧值。     
3. GET key 返回key所关联的字符串值,如果key不存在那么返回空。    
4. AUTH username password   
a. 服务器启动时读取当前目录下的配置文件auth.conf,里面记录了若干组用户和密码。    
b. 当用户密码匹配时,返回0,并且允许客户端执行URL命令。   
c. 当用户密码不匹配时,返回-1,并且不允许客户端执行URL命令。   
5. URL name url 。    
a. 当AUTH通过后才能运行此命令，否则返回空。    
b. name 是一个key,输入此命令后,如果这个key已持有值,则返回这两个值。如果没有,则server去拿到这个URL的HTTP状态和文件大小,将这两个值关联到name。   
6. 目前采用的是一个连接一个进程的多进程方式。

#### 客户端
##### python3 client.py CMD [PARAMETERS ... ]
1. 默认连接 localhost:5678 。可以通过--host和--port改变默认行为。   
2. 将用户输入的各种命令发送给服务器，并且显示服务器返回的结果。
