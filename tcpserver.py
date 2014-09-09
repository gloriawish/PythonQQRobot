from socket import *
from time import ctime
import time
import sys
import pymongo
from pymongo import Connection
from pymongo.errors import ConnectionFailure

HOST = ''
PORT = 8806
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def main():
    while True:
        print 'waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from:', addr

        while True:
            try:
                #data = tcpCliSock.recv(BUFSIZ)
                #if not data:
                #    break
                #print data
                time.sleep(2)
                tcpCliSock.send("ok")
            except Exception,e:
                print e
                tcpCliSock.close()
                break
    
main()
    
