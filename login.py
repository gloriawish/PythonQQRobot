# -*- coding: utf-8 -*-
import urllib
import urllib2
import httplib
import cookielib
import json
import re
import hashlib
import random
import time
import thread
from urllib import quote
from bs4 import BeautifulSoup
import Image


import hashlib

#对cookie进行支持
cj = cookielib.LWPCookieJar() 
cookie_support = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
urllib2.install_opener(opener)

#全局数据
sucessdata=None
#QQ="10588690"
groupuserlist=None
groupinfo=None
clientid=None

#-------------------http通信部分--------------------------
def Post(url,data,Host='d.web2.qq.com',Referer='http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2',Origin='http://d.web2.qq.com'):
    try:
        #resp = urllib2.urlopen(url)
        #postData = urllib.urlencode(data)
        postData=data
        req = urllib2.Request(url, postData)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_header('Accept','*/*')
        req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        req.add_header('Cache-Control', 'max-age=0')
        req.add_header('Connection', 'keep-alive')
        
        req.add_header('Host', Host)
        req.add_header('Referer', Referer)
        req.add_header('Origin', Origin)
        resp = urllib2.urlopen(req)
        return resp.read()
    except Exception,e:
        print e
    return None
'''
def Post(url,data):
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':'*/*',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip',
        'Connection':'Keep-Alive',
        'Referer':None
        }
    postData = urllib.urlencode(data)
    req = urllib2.Request(url,postData,header)
    resp = urllib2.urlopen(req)
    html = resp.read()
    return html
'''
def HttpPost(method,url,data={}):
    try:
        _urld = httplib.urlsplit(url)
        conn = httplib.HTTPConnection(_urld.netloc,80,True,3)
        conn.connect()
        data = urllib.urlencode(data)
        conn.putrequest("POST", url)
        conn.putheader("Content-Length", str(len(data)))
        conn.putheader("Content-Type", "application/x-www-form-urlencoded")
        conn.putheader("Connection", "close")
        conn.endheaders()
        if len(data)>0:
            conn.send(data)
        f = conn.getresponse()
        httpBody = f.read()
        f.close()
        conn.close()
    except Exception,e:
        print e
        return None
    
def Get(url):#,Host='d.web2.qq.com',Referer='http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2',Origin='http://d.web2.qq.com'
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
        
        
        req.add_header('Accept', '*/*')
        req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        req.add_header('Connection', 'keep-alive')
        #req.add_header("Content-Type", "utf-8")
        #req.add_header('Host', Host)
        #req.add_header('Referer', Referer)
        #req.add_header('Origin', Origin)
        #req.add_header('Host', 'ssl.ptlogin2.qq.com')
        resp = urllib2.urlopen(req)
        return resp.read()
    except Exception,e:
        print e
        return None
def Get2(url,Host,Referer,Origin):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
        
        
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        req.add_header('Cache-Control', 'max-age=0')
        req.add_header('Connection', 'keep-alive')
        req.add_header('Host', Host)
        req.add_header('Referer', Referer)
        req.add_header('Origin', Origin)
        #req.add_header('Host', 'ssl.ptlogin2.qq.com')
        resp = urllib2.urlopen(req)
        return resp.read()
    except Exception,e:
        print e
        return None
def HttpGet(url,data={}):
    try:
        _urld = httplib.urlsplit(url)
        conn = httplib.HTTPConnection(_urld.netloc,80,True,3)
        conn.connect()
        data = urllib.urlencode(data)
        conn.putrequest("GET", url, None)
        conn.putheader("Content-Length",'0')
        conn.putheader("Connection", "close")
        conn.endheaders()
        if len(data)>0:
            conn.send(data)
        f = conn.getresponse()
        httpBody = f.read()
        f.close()
        conn.close()
    except Exception,e:
        print e
        httpBody=''
    return httpBody
def GetImg(QQ):
    verify="https://ssl.captcha.qq.com/getimage?aid=1003903&r=0.9352272364776582&uin={QQ}&cap_cd=dVVYAA_4mvWhwy4O7UdJHI-yB2dJLrLR"
    verify=verify.replace('{QQ}',QQ)
    path= r"c:/verify/1.jpg"
    data = urllib.urlretrieve(verify,path)
    return data

def PCMd5(s):
    h=hashlib.md5()
    h.update(s)
    return h.hexdigest()
def hex2asc(s):
    _str="".join(s.split(r'\x'))
    length=len(_str)
    data=''
    for i in range(0,length,2):
        data+=chr(int(_str[i:i+2],16))
    return data

#------------------------QQ验证部分------------------------

verify="https://ssl.captcha.qq.com/getimage?aid=1003903&r=0.9352272364776582&uin={QQ}&cap_cd=dVVYAA_4mvWhwy4O7UdJHI-yB2dJLrLR"
verify=verify.replace('{QQ}','')



#检查时否需要验证码，和获取必要的参数
def CheckVerify(QQ):
    check="https://ssl.ptlogin2.qq.com/check?uin={QQ}&appid=1003903&js_ver=10080&js_type=0&login_sig=YPD0P*wu2n8vW1OS2f7VfzvPf3Ku5vnkP4nzImF0GybR02fsKZdjGYB7f9R7nQRn&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html&r=0.8179273759014904"
    check=check.replace('{QQ}',QQ)
    pattern=re.compile("ptui_checkVC\('(.*)','(.*)','(.*)'\);")
    result=Get(check)
    checked= pattern.search(result).groups()
    print 'CheckVerify'
    return checked


#V2 是 ptui_checkVC('0','!LJV','\x00\x00\x00\x00\x00\xa1\x92\x12') 第二个
#v1 是第一个参数
def PasswordSecret(password,v1,v2,md5=True):
    if md5==True:
        password=PCMd5(password).upper()
    length=len(password)
    temp=''
    for i in range(0,length,2):
        temp+=r'\x'+password[i:i+2]
    return PCMd5(PCMd5(hex2asc(temp)+hex2asc(v2)).upper()+v1).upper()

'''
ptuiCB('0','0','http://ptlogin4.web2.qq.com/check_sig?pttype=1&uin=10588690&service=login&nodirect=0&ptsig=aVtB1zP4gsbe-6XPRcKaXUIeUUKa3arIvq-5rSS5dbo_&s_url=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&f_url=&ptlang=2052&ptredirect=100&aid=1003903&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=1&pt_aid=0&pt_aaid=0&pt_light=0','0','登录成功！', '小竹');
'''
#第一次登陆
def Login(QQ,Password):
    #获取参数
    cheked=CheckVerify(QQ)
    #加密密码
    Pass=PasswordSecret(Password,cheked[1],cheked[2])
    loginurl="https://ssl.ptlogin2.qq.com/login?u={QQ}&p={PassWord}&verifycode={Verify}&webqq_type=10&remember_uin=1&login2qq=1&aid=1003903&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=4-30-135914&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10080&login_sig=YPD0P*wu2n8vW1OS2f7VfzvPf3Ku5vnkP4nzImF0GybR02fsKZdjGYB7f9R7nQRn&pt_uistyle=5"
    loginurl=loginurl.replace('{QQ}',QQ)
    #loginurl=loginurl.replace('{PassWord}',Pass)
    #loginurl=loginurl.replace('{Verify}',cheked[1])

    if(cheked[0]=="1"):
            #下载验证码
            GetImg(QQ)
            image = Image.open(r"c:/verify/1.jpg")
            image.show()
            code=raw_input("verify>")
            loginurl=loginurl.replace('{Verify}',code.upper())
            pwd=PasswordSecret(Password,r''+code,cheked[2])
            #pwd=self.PasswordSecret(pwd,cheked[1],cheked[2])
    else:
            loginurl=loginurl.replace('{Verify}',cheked[1])
            pwd=PasswordSecret(Password,cheked[1],cheked[2])
        
    loginurl=loginurl.replace('{PassWord}',pwd)

    result=Get(loginurl)
    print 'Login'
    pattern=re.compile("ptuiCB\('(.*)','(.*)','(.*)','(.*)','(.*)',\s'(.*)'\);")
    ret= pattern.search(result).groups()
    #获取必要的cookie 否则第二次登陆会出错
    Get(ret[2])
    print 'cookie'
    ptwebqq=None
    for c in cj:
        if c.name=="ptwebqq":
            ptwebqq=c.value
    return ptwebqq,result

'''{"retcode":0,
"result":{
          "uin":10588690,
          "cip":1707901841,
          "index":1075,
          "port":59571,
          "status":"online",
          "vfwebqq":"c043f1f6ce5c3b76a4603ab60082668bef2dde0b987808f728e2071eb7c164eeb30fcd85c31018d2",
          "psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363000006cb000001ae1036200a192126d0000000a40356c593742635175316d00000028c043f1f6ce5c3b76a4603ab60082668bef2dde0b987808f728e2071eb7c164eeb30fcd85c31018d2",
          "user_state":0,
          "f":0
          }
}'''
#第二次登陆
def Login2(ptwebqq):
    clientid=random.randint(1000000,10000000)
    url="http://d.web2.qq.com/channel/login2"
    postdata="r=%7B%22status%22%3A%22online%22%2C%22ptwebqq%22%3A%22{$ptwebqq}%22%2C%22passwd_sig%22%3A%22%22%2C%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3Anull%7D&clientid={$clientid}&psessionid=null"
    postdata=postdata.replace("{$ptwebqq}",ptwebqq)
    postdata=postdata.replace("{$clientid}",str(clientid))
    print 'Login2'
    return clientid,Post(url,postdata)
#心跳包
def HeartBreak(clientid,psessionid):
    url="http://d.web2.qq.com/channel/poll2"
    postdata="r=%7B%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3A%22{$psessionid}%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid={$clientid}&psessionid={$psessionid}"
    postdata=postdata.replace("{$clientid}",str(clientid))
    postdata=postdata.replace("{$psessionid}",psessionid)
    while True:
        #每隔2秒发送心跳包
        #Post(url,postdata)
        #print "HeartBreak"
        ret=Post(url,postdata)
        try:
            retjson=json.loads(ret)
            retjson=retjson["result"]
            retjson=retjson[0]
            if(retjson["poll_type"]=="group_message"):
                msg=retjson["value"]
                ProcessMsg(msg)
        except Exception,e:
            print e
        time.sleep(2)
def QQLogin():
    #第一次登陆
    ptwebqq,result=Login("10588690","1992128ZJ")
    #第二次登陆 返回clientid 和有用的json数据
    clientid,ret=Login2(ptwebqq)
    retjson=json.loads(ret)
    retjson=retjson["result"]
    #开启心跳线程
    #thread.start_new_thread(HeartBreak,(clientid,retjson["psessionid"],))
    return clientid,retjson

def GetGroupNameList(vfwebqq):
    url="http://s.web2.qq.com/api/get_group_name_list_mask2"
    postdata="r=%7B%22vfwebqq%22%3A%22{$vfwebqq}%22%7D"
    postdata=postdata.replace("{$vfwebqq}",vfwebqq)
    host='s.web2.qq.com'
    origin='http://s.web2.qq.com'
    ref='http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=3'
    ret=Post(url,postdata,host,ref,origin)
    print 'GetGroup'
    retjson=json.loads(ret)
    retjson=retjson["result"]
    return retjson

def GetFriendList(vfwebqq):
    hash=None
    url="http://s.web2.qq.com/api/get_user_friends2"
    postdata="r=%7B%22h%22%3A%22hello%22%2C%22hash%22%3A%22{hash}%22%2C%22vfwebqq%22%3A%22{$vfwebqq}%22%7D"
    
    postdata=postdata.replace("{$vfwebqq}",vfwebqq)
    postdata=postdata.replace("{$hash}",hash)
    host='s.web2.qq.com'
    origin='http://s.web2.qq.com'
    ref='http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=3'
    Post(url,postdata,host,ref,origin)

def GetGroupInfo(gcode,vfwebqq):
    url="http://s.web2.qq.com/api/get_group_info_ext2?gcode={$gcode}&cb=undefined&vfwebqq={$vfwebqq}&t=1402069438458"
    url=url.replace("{$vfwebqq}",vfwebqq)
    url=url.replace("{$gcode}",str(gcode))
    host='s.web2.qq.com'
    ref='http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=3'
    ret=Get2(url,host,ref,None)
    print "GetGroupInfo"
    return json.loads(ret)

#发送消息
def SendGroupMsg(groupid,msg,psessionid,clientid):
    #msg=quote(msg.encode('utf8'))#msg.decode('cp936').encode('utf8')
    msg='1'
    url="http://d.web2.qq.com/channel/send_qun_msg2"
    msg_id = 77860003

    #postdata="r=%7B%22group_uin%22%3A{$group_id}%2C%22content%22%3A%22%5B%5C%22{$msg}%22%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%5C%22%3A%5C%22%E5%AE%8B%E4%BD%93%5C%22%2C%5C%22size%5C%22%3A%5C%2210%5C%22%2C%5C%22style%5C%22%3A%5B0%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22000000%5C%22%7D%5D%5D%22%2C%22msg_id%22%3A{$msg_id}%2C%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3A%22{$psessionid}%22%7D&clientid={$clientid}&psessionid={$psessionid}"
    postdata="r=%7B%22group_uin%22%3A{$group_uin}%2C%22content%22%3A%22%5B%5C%22{$msg}%5C%22%2C%5C%22%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%5C%22%3A%5C%22%E5%AE%8B%E4%BD%93%5C%22%2C%5C%22size%5C%22%3A%5C%2210%5C%22%2C%5C%22style%5C%22%3A%5B0%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22000000%5C%22%7D%5D%5D%22%2C%22msg_id%22%3A{$msg_id}%2C%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3A%22{$psessionid}%22%7D&clientid={$clientid}&psessionid={$psessionid}"
    postdata=postdata.replace("{$group_uin}",str(groupid))
    postdata=postdata.replace("{$psessionid}",psessionid)
    postdata=postdata.replace("{$clientid}",str(clientid))
    postdata=postdata.replace("{$msg_id}",str(msg_id))
    postdata=postdata.replace("{$msg}",msg)
    
    Post(url,postdata)
    print "send msg: "+msg
def GetGroupFromList(groupret):
    dic={}
    for group in groupret['gnamelist']:
        if group['name']==u"10级计算机软件工程":
            print group['name']
            dic["groupname"]=group['name']
            dic["groupid"]=group['gid']
            dic["groupcode"]=group['code']
            return dic
#获取群用户的名片
def FindGroupUserName(uin):
    userlist=groupuserlist["result"]
    cardlist=userlist["cards"]
    for card in cardlist:
        if card['muin']==uin:
            return card['card']
def ProcessMsg(msg):
    reply_ip=msg['reply_ip']
    group_code=msg['group_code']
    send_uin=msg['send_uin']
    from_uin=msg['from_uin']
    to_uin=msg['to_uin']
    content=msg["content"]
    #回复消息
    SendGroupMsg(groupinfo['groupid'],str(content[1]),sucessdata['psessionid'],clientid)
    print FindGroupUserName(send_uin),":",content[1]

clientid,sucessdata=QQLogin()
groupret=GetGroupNameList(sucessdata['vfwebqq'])

#保存group相关信息
groupinfo=GetGroupFromList(groupret)
#群用户列表
groupuserlist=GetGroupInfo(groupinfo["groupcode"],sucessdata['vfwebqq'])

print "login sucess..."

while True:
    #SendGroupMsg(mygid,msg,sucessdata['psessionid'],clientid)
    HeartBreak(clientid,sucessdata['psessionid'])
    time.sleep(3)


