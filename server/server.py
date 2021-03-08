#! /usr/bin/env python3
# Echo server program

buff= ""
nextChar = 0
limit = 0

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

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
        send(fileName)
        conn.shutdown(socket.SHUT_WR)


def send(fileName):
    while cont:
        numLines+=1
        os.write(1,ps1.encode())
        line=getLine()
        length=len(line)
        if(line == "0"):
            cont=False
        else:
            conn.send(b (length":"line))
        return 1;
def getChar():
    global nextChar
    global limit
    global buff
    
    if(nextChar==limit): 
        nextChar = 0
        buffByte = os.read(0,1000)
        buff=str(buffByte, 'utf-8')
        limit=len(buff)

        if(limit==0):
            
            return 0

    c=buff[nextChar]

    if(c=="\n"):
            
        limit=0
        buff=""  
        nextChar=0
        return -1

    else:

        nextChar+=1
        return c

def getLine():

    line=""
    c=getChar()                                                                                   

    while(c!=0 and c != -1 ):

        line +=c                                              
        c=getChar()
        
    if(len(line)>0):

        return line

    else:

        return "0"
        
def myOpen(fileName): #open our files to be able to read them
    try:
        
        fd_in = os.open(fileName, os.O_RDWR) #open and read the file
        buff = os.read(fd_in,1024)
        os.close(fd_in)
        return buff
    
    except FileNotFoundError:
        
        os.write(1,('File was not found').encode())
        sys.exit(1)
