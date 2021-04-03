#! /usr/bin/env python3
# Echo client program
state=0
import os,socket, sys, re, time
sys.path.append("../lib")       # for params
import params
from mySocket import *


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")

while 1:
    if(state==0):
        found=True;
        while found:
            os.write(1,("Select [send][recieve][exit]").encode())
            response=myLine().lower()
            if(response=="send" or response=="receive" or response=="exit"):
               found=False;
        
        if(response=="send"):
            state=1
        elif(response=="exit"):
            state=3
        else:
            state=2
    elif (state==1):
        s.send(("receive").encode())              #server will recieve 
        os.write(1,("Please enter file Name").encode())
        fileName=myLine()                         #getting the name of the file i will send
        send(s,fileName)                          #sending the file
        state=0
    elif (state==2):
        s.send(("send").encode())                 #server will send the file to me
        os.write(1,("Please enter file Name").encode())
        fileName=myLine()
        s.send((fileName).encode())               #telling the server what file i want
        recv(s)                                   #starting to receive
        state=0
    else:
        print("done")
        sys.exit(1)
