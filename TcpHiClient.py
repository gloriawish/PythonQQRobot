from socket import *
import json

HOST = '127.0.0.1'
PORT = 8874
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = raw_input('> ')
    if data=="send":
        data = raw_input('msg:')
        data=data.decode('gbk').encode('utf8')
        msg=json.dumps({"cmd":"send","data":data})
        tcpCliSock.send(msg)
    elif data=="iscopy":
        msg=json.dumps({"cmd":"iscopy"})
        tcpCliSock.send(msg)
    elif data=="nocopy":
        msg=json.dumps({"cmd":"nocopy"})
        tcpCliSock.send(msg)
    elif data=="isauto":
        msg=json.dumps({"cmd":"isauto"})
        tcpCliSock.send(msg)
    elif data=="noauto":
        msg=json.dumps({"cmd":"noauto"})
        tcpCliSock.send(msg)
    elif data=="isrobot":
        msg=json.dumps({"cmd":"isrobot"})
        tcpCliSock.send(msg)
    elif data=="norobot":
        msg=json.dumps({"cmd":"norobot"})
        tcpCliSock.send(msg)
tcpCliSock.close()
