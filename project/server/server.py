#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
sys.path.append("..")
from mySocket import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        data = conn.recv(1024).decode()
        if(data=="send"):                 #server needs too send the file
            fileName=conn.recv(1024).decode() #client tells server what to send
            send(conn,fileName)
        elif(data=="receive"):            #server will recieve the file
                recv(conn)
        else:                             #something went wrong close
                conn.shutdown(socket.SHUT_WR)
    else:
            print("eror at fork")
