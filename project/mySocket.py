#! /usr/bin/env python3
import os, sys, time, re, array, socket

buff= ""
lBuff= ""
nextChar = 0
limit = 0
lLimit = 0
nextLine = 0

def getChar():
    
    global nextChar
    global limit    
    global buff
    print("this is the char location and the limit "+ str(nextChar)+ "  "+str(limit))  
    if(nextChar==limit):
        
        nextChar = 0
        buffByte = os.read(0,1024)
        buff=buffByte.decode()
        print("this is the buffer "+buff)
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

def myLine():

    line=""
    c=getChar()
    while(c!=0 and c!=-1):
        line += c    
        c=getChar()        
    if(len(line)>0):            
        return line
    elif(c==0):        
        return 0
    else:
        return -1

def getBuff(fd):
    
    global nextChar
    global limit    
    global buff
    if(nextChar==limit):
        
        nextChar = 0
        if(fd!=0):
            buffByte = os.read(fd,1024)
        buff=buffByte.decode()
        limit=len(buff)        
        if(limit==0):
            return 0        
    c=buff[nextChar]        
    nextChar+=1
    return c

def sendBuff(fd):

    line=""
    c=getBuff(fd)
    while(c!=0):
        line += c    
        c=getBuff(fd)        
    if(len(line)>0):            
        return line
    elif(c==0):        
        return 0
    else:
        return -1

def myPrint(string): 
    os.write(1, (string + '\n').encode())

def myOpen(fileName):
    try:
        path=fileName
        fd = os.open(path, os.O_RDWR)                                     
        return fd
                                                
    except FileNotFoundError:
        
        myPrint('File was not found')
        print(path)
        sys.exit(1)


def reDirectInput():
    global inFile
    os.close(0)                 # redirect child's stdout
    os.open(inFile, os.O_RDONLY);
    os.set_inheritable(0, True)
    return args



def reDirectOutput():
    global outFile
    os.close(1)                 # redirect child's stdout
    os.open(outFile, os.O_CREAT | os.O_WRONLY);
    os.set_inheritable(1, True)
    

def myWrite(fileName, buff):
    os.write(1, buff.encode()) 

def send(s,fileName): 
    
    fd1=myOpen(fileName)
    s.send(("name:"+fileName).encode())
    cont=True
    while cont: 
        line=sendBuff(fd1)
        if(line==0):
            s.send(("done:done").encode())
            cont=False
            os.close(fd1)
            myPrint("Done")
        else:
            lenght=len(line)
            s.send((str(lenght)+":"+line).encode())
                   
def recv(s):
    myPrint ("receiving")
    cont=True;
    while cont:
        
        line=s.recv(1024).decode()
        component=line.split(":")
        size=component[0].replace(":","");
        data=component[1]
        if(size=="name"):
            path=data
            fd2=os.open(path,os.O_RDWR|os.O_CREAT)
        elif(size=="done"):
            os.close(fd2)
            cont=False
        else:
            myPrint("writing")
            numBytes= os.write(fd2, data.encode())
            totalBytes=+numBytes;
            
