'''
Created on 2013-3-29

@author: VTX
'''

import socket

HOST = ""
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept();

print "Connected by", addr
while 1:
    data = conn.recv(1024)
    print data
    if not data:
        break
    conn.sendall(data)
conn.close()
