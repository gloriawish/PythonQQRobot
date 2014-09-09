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
import threading
from urllib import quote
from urllib import unquote
from bs4 import BeautifulSoup
import hashlib
import Tool
import Image
import types
from socket import *
from hash import newhash
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()
HOST = ''
PORT = 8874
BUFSIZE = 1024
ADDR = (HOST, PORT)
class QQRobot():
    #全局的常量
    HOST=['d.web2.qq.com','s.web2.qq.com']
    REFERER=['http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2','http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=3']
    ORIGIN=['http://d.web2.qq.com','http://s.web2.qq.com']
    TIMES=0
    """description of class"""
    def __init__(self, QQ=None, PassWord=None):
        self.QQ=QQ
        self.PassWord=PassWord
        #二次登陆返回的结果集
        self._sucessdata=None
        #获取群列表的结果集 在字段 'gnamelist'
        self.grouplist=None
        #当前所在群的信息
        self.groupinfo={}
        #获取群的用户列表 在字段'result'
        self.groupuserlist=None
        
        #获取的好友信息保存
        self.friends=None
        #第一次访问产生的cookie中的
        self.ptwebqq=None
        #登录过程中需要的客户端id
        self.clientid=random.randint(1000000,10000000)

        #复读机模式
        self.iscopy=True
        #自动发送消息
        self.auto=False
        #机器人自动回复消息
        self.isrobot=True
        #对cookie进行支持
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cj),
                )
        urllib2.install_opener(self.opener)
        #socket
        self.tcpSerSock=socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(ADDR)
        self.tcpSerSock.listen(5)
        
        #客户端的scoket引用
        self.tcpCliSock=None
        #客户端是否连接上来了
        self.isconnect=False
        
    #post 请求
    def Post(self,url,data,Host=None,Referer=None,Origin=None):
        try:
            #postData = urllib.urlencode(data)
            postData = data
            req = urllib2.Request(url, postData)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            req.add_header('Accept','*/*')
            req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            req.add_header('Cache-Control', 'max-age=0')
            req.add_header('Connection', 'keep-alive')
            if Host!=None:
                req.add_header('Host', Host)
            if Referer!=None:
                req.add_header('Referer', Referer)
            if Origin!=None:
                req.add_header('Origin', Origin)
            resp = urllib2.urlopen(req,postData)
            return resp.read()
        except Exception,e:
            print "post error "+str(e)
            return None
    #get请求
    def Get(self,url,Host=None,Referer=None,Origin=None):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
            req.add_header('Accept', '*/*')
            req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            req.add_header('Connection', 'keep-alive')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            if Host!=None:
                req.add_header('Host', Host)
            if Referer!=None:
                req.add_header('Referer', Referer)
            if Origin!=None:
                req.add_header('Origin', Origin)
            resp = urllib2.urlopen(req)
            return resp.read()
        except Exception,e:
            print "get error "+str(e)
            return None
    def GetVerify(self):
        #url = 'https://ssl.captcha.qq.com/getimage?&uin='+str(self.QQ)+'&aid=1002101&0.45644426648505' + str(random.randint(10,99))
        verify="https://ssl.captcha.qq.com/getimage?aid=1003903&r=0.6472875226754695&uin={QQ}&cap_cd=aSD-ZVcNEcozlZUurhNYhp-MBHf4hjbJ"
        verify=verify.replace('{QQ}',self.QQ)
        path= r"c:/verify/1.jpg"
        #data = urllib.urlretrieve(url,path)
        data = urllib2.urlopen(verify)
        localPic =open(r"c:/verify/1.jpg",'wb') 
        localPic.write(data.read()) 
        localPic.close() 
        data.close() 
    #md5加密函数
    def PCMd5(self,s):
        h=hashlib.md5()
        h.update(s)
        return h.hexdigest()
    #16进制转字符
    def hex2asc(self,s):
        _str="".join(s.split(r'\x'))
        length=len(_str)
        data=''
        for i in range(0,length,2):
            data+=chr(int(_str[i:i+2],16))
        return data
    #--------开始登录--------
    #检查时否需要验证码，和获取必要的参数
    '''
    返回值 ptui_checkVC('0','!NTZ','\x00\x00\x00\x00\x22\x79\x9f\x0d', 'ef0e577a40249cc2b77dc9f266a3a4141a987d06a8f3ae39117183f1ff0491720e1f6f498a9a038f032d99f8622ea628');
    '''
    def CheckVerify(self,uin):
        check="https://ssl.ptlogin2.qq.com/check?uin={uin}&appid=1003903&js_ver=10092&js_type=0&login_sig=K5F0E8woS74td4sRIqKiSHmH6B2RYYP467z2r*6YWaH4wc7vE*4G*X7V2kGP9s1*&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html&r=0.2689784204121679"
        check=check.replace('{uin}',uin)
        pattern=re.compile("ptui_checkVC\('(.*)','(.*)','(.*)', '(.*)'\);")
        result=self.Get(check)
        checked= pattern.search(result).groups()
        print 'Step1: CheckVerify'
        self.SendMsg('Step1: CheckVerify')
        return checked
    #密码加密函数
    '''
    v1 是  第一个参数
    V2 是  第二个
    session 是第三个
    ptui_checkVC('0','!NTZ','\x00\x00\x00\x00\x22\x79\x9f\x0d', 'ef0e577a40249cc2b77dc9f266a3a4141a987d06a8f3ae39117183f1ff0491720e1f6f498a9a038f032d99f8622ea628');
    '''
    def PasswordSecret(self,password,v1,v2,md5=True):
        if md5==True:
            password=self.PCMd5(password).upper()
        length=len(password)
        temp=''
        for i in range(0,length,2):
            temp+=r'\x'+password[i:i+2]
        return self.PCMd5(self.PCMd5(self.hex2asc(temp)+self.hex2asc(v2)).upper()+v1).upper()

    #第一次登陆
    '''
    return ptuiCB('0','0','http://ptlogin4.web2.qq.com/check_sig?pttype=1&uin=578395917&service=login&nodirect=0&ptsig=uV34Xt9XM3e2oQ3wuub8LIBIGsIIZATjiz-cqSVHJ5o_&s_url=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html%3Flogin2qq%3D0%26webqq_type%3D10&f_url=&ptlang=2052&ptredirect=100&aid=1003903&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=1&pt_aid=0&pt_aaid=0&pt_light=0','0','登录成功！', '夜迷离、');

    '''
    def Login(self,uin,pwd):
        #获取参数

        cheked=self.CheckVerify(uin)
        #加密密码
        loginurl="https://ssl.ptlogin2.qq.com/login?u={uin}&p={pwd}&verifycode={verify}&webqq_type=10&remember_uin=1&login2qq=0&aid=1003903&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html%3Flogin2qq%3D0%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=2-9-33854&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10092&login_sig=K5F0E8woS74td4sRIqKiSHmH6B2RYYP467z2r*6YWaH4wc7vE*4G*X7V2kGP9s1*&pt_uistyle=5&pt_vcode_v1=0&pt_verifysession_v1={session}"
        loginurl=loginurl.replace('{uin}',uin)
        #2014-8-29  发现有多加了一个参数
        loginurl=loginurl.replace('{session}',cheked[3])
        if(cheked[0]=="1"):
            #下载验证码
            self.GetVerify()
            image = Image.open(r"c:/verify/1.jpg")
            image.show()
            code=raw_input("verifycode:").strip()
            loginurl=loginurl.replace('{verify}',code.upper())
            pwd=self.PasswordSecret(pwd,r''+code.upper(),cheked[2])
        else:
            loginurl=loginurl.replace('{verify}',cheked[1])
            pwd=self.PasswordSecret(pwd,cheked[1],cheked[2])
        
        loginurl=loginurl.replace('{pwd}',pwd)
        print uin,pwd,cheked[1]

        result=self.Get(loginurl,'ssl.ptlogin2.qq.com','https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=5&mibao_css=m_webqq&appid=1003903&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html&f_url=loginerroralert&strong_login=0&login_state=10&t=20140612002',None)

        print 'Step2: Login'
        self.SendMsg('Step2: Login')
        pattern=re.compile("ptuiCB\('(.*)','(.*)','(.*)','(.*)','(.*)',\s'(.*)'\);")
        ret= pattern.search(result).groups()
        if ret[0]!="0":
            return False
        #获取必要的cookie 否则第二次登陆会出错
        self.Get(ret[2])
        print 'Step3: GetCookie'
        self.SendMsg('Step3: GetCookie')
        for c in self.cj:
            if c.name=="ptwebqq":
                self.ptwebqq=c.value
                return True
        return False

    #第二次登陆
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
    def Login2(self):
        try:
            url="http://d.web2.qq.com/channel/login2"

            #postdata="r=%7B%22status%22%3A%22online%22%2C%22ptwebqq%22%3A%22{$ptwebqq}%22%2C%22passwd_sig%22%3A%22%22%2C%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3Anull%7D&clientid={$clientid}&psessionid=null"
            #postdata=postdata.replace("{$ptwebqq}",self.ptwebqq)
            #postdata=postdata.replace("{$clientid}",str(self.clientid))
            
            r={
              "status":"online",
              "ptwebqq":self.ptwebqq,
              "passwd_sig":"",
              "clientid":str(self.clientid),
              "psessionid":None,
              }
            r=json.dumps(r)
            data = {
                    "r":r,
                    "psessionid":None,
                    "clientid":self.clientid,
                }
            postdata=urllib.urlencode(data)
            postdata=postdata.replace("+","")
            
            print 'Step4: Login2'
            self.SendMsg('Step4: Login2')
            result=self.Post(url,postdata,QQRobot.HOST[0],QQRobot.REFERER[0],QQRobot.ORIGIN[0])
            retjson=json.loads(result)
            retjson=retjson["result"]
            return retjson
        except Exception,e:
                print "Login2 error "+str(e)
    #心跳包
    '''
    {"retcode":0,"result":[{"poll_type":"group_message","value":{"msg_id":12262,"from_uin":3254502432,"to_uin":10588690,"msg_id2":570347,"msg_type":43,"reply_ip":176886376,"group_code":3011786712,"send_uin":3623747568,"seq":96596,"time":1402532154,"info_seq":116761379,"content":[["font",{"size":10,"color":"000000","style":[0,0,0],"name":"\u5B8B\u4F53"}],"\u3002\u3002\u3002\u3002 "]}}]}

    '''
    def HeartBreak(self,psessionid):
        url="http://d.web2.qq.com/channel/poll2"
        #postdata="r=%7B%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3A%22{$psessionid}%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid={$clientid}&psessionid={$psessionid}"
        #postdata=postdata.replace("{$clientid}",str(self.clientid))
        #postdata=postdata.replace("{$psessionid}",psessionid)
        r={
          "clientid":str(self.clientid),
          "psessionid":psessionid,
          "key":0,
          "ids":[]
          }
        r=json.dumps(r)
        data = {
                "r":r,
                "psessionid":psessionid,
                "clientid":self.clientid,
            }
        postdata=urllib.urlencode(data)
        postdata=postdata.replace("+","")
        while True:
            #每隔2秒发送心跳包
            ret=self.Post(url,postdata,QQRobot.HOST[0],QQRobot.REFERER[0],QQRobot.ORIGIN[0])
            try:
                retjson=json.loads(ret)
                retjson=retjson["result"]
                retjson=retjson[0]
                #print "heartbreak"
                if(retjson["poll_type"]=="group_message"):
                    msg=retjson["value"]
                    self.ProcessMsg(msg)
            except Exception,e:
                #print "HeartBreak error "+str(e)
                pass
            time.sleep(2)
    #获取群列表信息
    def GetGroupNameList(self,vfwebqq):
        try:
            url="http://s.web2.qq.com/api/get_group_name_list_mask2"
            #postdata="r=%7B%22vfwebqq%22%3A%22{$vfwebqq}%22%7D"
            #postdata=postdata.replace("{$vfwebqq}",vfwebqq)
            hash=newhash(self.QQ, self.ptwebqq)
            r={
               "hash":hash,
               "vfwebqq":vfwebqq,
               }
            r=json.dumps(r)
            data = {
                    "r":r,
                    }
            postdata=urllib.urlencode(data)
            postdata=postdata.replace("+","")
            
            
            
            ret=self.Post(url,postdata,QQRobot.HOST[1],QQRobot.REFERER[1],QQRobot.ORIGIN[1])
            print 'Step5: GetGroupList'
            self.SendMsg('Step5: GetGroupList')
            retjson=json.loads(ret)
            retjson=retjson["result"]
            self.grouplist=retjson
            for group in self.grouplist['gnamelist']:
                print group["code"],group["name"]
                msgrecord=str(group["code"])+" "+group["name"]
                self.SendMsg(msgrecord.encode("utf8"))
                
        except Exception,e:
            print "GetGroupNameList error"+str(e)
    #获取群成员信息
    def GetGroupInfo(self,gcode,vfwebqq):
        try:
            url="http://s.web2.qq.com/api/get_group_info_ext2?gcode={$gcode}&vfwebqq={$vfwebqq}&t=1409288226118"
            url=url.replace("{$vfwebqq}",vfwebqq)
            url=url.replace("{$gcode}",str(gcode))
            ret=self.Get(url,QQRobot.HOST[1],QQRobot.REFERER[1],None)
            print "Step6: GetGroupInfo"
            self.SendMsg('Step6: GetGroupInfo')
            retjson=json.loads(ret)
            retjson=retjson["result"]
            self.groupuserlist=retjson
        except Exception,e:
            print "GetGroupInfo error"+str(e)
            
    def GetSelfInfo(self,vfwebqq):
        try:
            url="http://s.web2.qq.com/api/get_friend_info2?tuin={$uin}&verifysession=&code=&vfwebqq={$vfwebqq}&t=1402534798024"
            url=url.replace("{$vfwebqq}",vfwebqq)
            url=url.replace("{$uin}",str(self.QQ))
            ret=self.Get(url,QQRobot.HOST[1],QQRobot.REFERER[1],None)
            retjson=json.loads(ret)
            print retjson
        except Exception,e:
            print str(e)
    #获取好友信息
    def GetFriendList(self):
        hash=newhash(self.QQ, self.ptwebqq)
        url="http://s.web2.qq.com/api/get_user_friends2"
        #postdata="r=%7B%22h%22%3A%22hello%22%2C%22hash%22%3A%22{$hash}%22%2C%22vfwebqq%22%3A%22{$vfwebqq}%22%7D"
        #postdata=postdata.replace("{$hash}",hash)
        #postdata=postdata.replace("{$vfwebqq}",self._sucessdata["vfwebqq"])
        r={
          "h":"hello",
          "hash":hash,
          "vfwebqq":self._sucessdata["vfwebqq"],
          }
        r=json.dumps(r)
        data = {
                "r":r,
            }
        postdata=urllib.urlencode(data)
        postdata=postdata.replace("+","")
        
        
        ret=self.Post(url,postdata,QQRobot.HOST[1],QQRobot.REFERER[1],QQRobot.ORIGIN[1])
        retjson=json.loads(ret)
        retjson=retjson["result"]
        self.friends=retjson
        #有备注名的好友
        marknames=retjson["marknames"]
        #无备注名的好友
        info=retjson["info"]
        for m in marknames:
            try:
                 print m["uin"],m["markname"]
                 msgrecord=str(m["uin"])+" "+m["markname"]
                 self.SendMsg(msgrecord.encode("utf8"))
            except:
                 print "the marknames name is wrong"
        for i in info:
            try:
                print i["uin"],i["nick"]
                msgrecord=str(i["uin"])+" "+i["nick"]
                self.SendMsg(msgrecord.encode("utf8"))
            except:
                 print "the info name is wrong"
            
    def SendPersonMsg(self,msg,touin,psessionid):
        url="http://d.web2.qq.com/channel/send_buddy_msg2"
        postdata="r=%7B%22to%22%3A{$touin}%2C%22face%22%3A561%2C%22content%22%3A%22%5B{$msg}%2C%5C%22%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%5C%22%3A%5C%22%E5%AE%8B%E4%BD%93%5C%22%2C%5C%22size%5C%22%3A%5C%2210%5C%22%2C%5C%22style%5C%22%3A%5B0%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22000000%5C%22%7D%5D%5D%22 %2C%22msg_id%22%3A{$msg_id}%2C%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3A%22{$psessionid}%22%7D&clientid={$clientid}&psessionid={$psessionid}"
        
        #封装消息
        msg_id = random.randint(1000000,10000000)
        style="%5C%22{content}%5C%22"
        temp=""
        temp=style.replace("{content}",quote(c.encode('utf8')))
        urlmsg=temp
        postdata=postdata.replace("{$touin}",str(touin))
        postdata=postdata.replace("{$psessionid}",psessionid)
        postdata=postdata.replace("{$clientid}",str(self.clientid))
        postdata=postdata.replace("{$msg_id}",str(msg_id))
        postdata=postdata.replace("{$msg}",urlmsg)
        self.Post(url,postdata,QQRobot.HOST[0],QQRobot.REFERER[0],QQRobot.ORIGIN[0])
        
    #发送群消息
    def SendGroupMsg(self,groupid,msg,psessionid):
        try:
            '''
            style="%5C%22{content}%5C%22"
            temp=""
            part=""
            for c in msg:
                if type(c) is types.ListType:
                    
                    part=quote(str(c).strip().encode('utf8'))+"%2C"
                    #part=part.replace("%20","")
                    part=part.replace("%27","%5C%22") #把 ' 换为 \"
                    part=part.replace("u","") #把 u 换为 空
                    temp+=part
                else:
                    temp+=style.replace("{content}",quote(c.encode('utf8')))+"%2C"
            temp=temp[0:len(temp)-3]
            '''
            #把普通字符串包裹起来
            style="\"{content}\""
            temp=""
            part=""
            for c in msg:
                if type(c) is types.ListType:
                    part=quote(str(c).strip().encode('utf8'))+","
                    part=part.replace("'","\"") #把 ' 换为 \"
                    part=part.replace("u","") #把 u 换为 空
                    temp+=part
                else:
                    temp+=style.replace("{content}",c.encode('utf8'))+","
                    #temp+=style.replace("{content}",quote(c.encode('utf8')))+","
            temp=temp[0:len(temp)-1]
            
            url="http://d.web2.qq.com/channel/send_qun_msg2"
            msg_id = 77860003
            #postdata="r=%7B%22group_uin%22%3A{$group_uin}%2C%22content%22%3A%22%5B{$msg}%2C%5C%22%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%5C%22%3A%5C%22%E5%AE%8B%E4%BD%93%5C%22%2C%5C%22size%5C%22%3A%5C%2210%5C%22%2C%5C%22style%5C%22%3A%5B0%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22000000%5C%22%7D%5D%5D%22%2C%22msg_id%22%3A{$msg_id}%2C%22clientid%22%3A%22{$clientid}%22%2C%22psessionid%22%3A%22{$psessionid}%22%7D&clientid={$clientid}&psessionid={$psessionid}"
            #postdata=postdata.replace("{$group_uin}",str(groupid))
            #postdata=postdata.replace("{$psessionid}",psessionid)
            #postdata=postdata.replace("{$clientid}",str(self.clientid))
            #postdata=postdata.replace("{$msg_id}",str(msg_id))
            #postdata=postdata.replace("{$msg}",urlmsg)
            content="[{$msg},\"\",[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]"
            content=content.replace("{$msg}",temp)
            r={
              "group_uin":str(groupid),
              "content":content,
              "msg_id":str(msg_id),
              "clientid":str(self.clientid),
              "psessionid":psessionid
              }
            r=json.dumps(r)
            data = {
                    "r":r,
                    "psessionid":psessionid,
                    "clientid":self.clientid,
                }
            postdata=urllib.urlencode(data)
            postdata=postdata.replace("+","")
            
            self.Post(url,postdata,QQRobot.HOST[0],QQRobot.REFERER[0],QQRobot.ORIGIN[0])
        except Exception,e:
            print "SendGroupMsg error"+str(e)
        #print "send msg: "+str(msg)
    def GetGroupFromList(self,groupname):
        for group in self.grouplist['gnamelist']:
            name=unicode(groupname,'utf-8')
            if group['name']==name:
                print name
                self.groupinfo["groupname"]=group['name']
                self.groupinfo["groupid"]=group['gid']
                self.groupinfo["groupcode"]=group['code']
                return self.groupinfo
    def FindGroupFromList(self,groupcode):
        for group in self.grouplist['gnamelist']:
            if int(group['code'])==int(groupcode):
                print group['name']
                self.groupinfo["groupname"]=group['name']
                self.groupinfo["groupid"]=group['gid']
                self.groupinfo["groupcode"]=group['code']
                return True
        return False
    #获取群用户的名片
    def FindGroupUserName(self,uin):
        cardlist=self.groupuserlist["cards"]
        for card in cardlist:
            if card['muin']==uin:
                return card['card']
    def ShowGroupUser(self):
        cardlist=self.groupuserlist["cards"]
        for card in cardlist:
            #self.SendMsg(card['card'])
            print card['card']
        print "-----------"
    #处理心跳包返回数据
    def ProcessMsg(self,msg):
        try:
            reply_ip=msg['reply_ip']
            group_code=msg['group_code']
            send_uin=msg['send_uin']
            from_uin=msg['from_uin']
            to_uin=msg['to_uin']
            if len(msg["content"])<=2:
                content=msg["content"][1]
            else:
                content=msg["content"][1:-1]
            if group_code==self.groupinfo['groupcode']:
                
                msgrecord=self.FindGroupUserName(send_uin)+":"+content
                print msgrecord
                msgrecord=msgrecord.encode('utf8')
                self.SendMsg(msgrecord);
                #只显示同一个群的消息
                if self.iscopy==True and self.isrobot==True:
                    if type(content) is not types.ListType:
                        pass
                        #msg=Tool.GetAutoAnswer(content)#获取机器人消息
                        #msg=unicode(msg,"utf-8");
                        #print msg
                        #self.SendMsg(msg.encode('utf8'));
                        #self.SendGroupMsg(self.groupinfo['groupid'],msg,self._sucessdata['psessionid'])
                elif self.iscopy==True and self.isrobot==False:
                    self.SendGroupMsg(self.groupinfo['groupid'],content,self._sucessdata['psessionid'])
        except Exception,e:
            print str(e)
            pass
    def AutoSendMessage(self):
        content=[u"哟西,签到",u"hi 我是新人",u"我是来刷等级的",u"诶，好无聊啊",u"哪个讲个笑话来听",u"赚积分",u"来人啊",u"我是复读机",u"哈哈 我是机器人",u"刷级神器,没有想不到只有做不到"]
        while True:
            if self.auto:
                _content=content[QQRobot.TIMES%10]
                QQRobot.TIMES=QQRobot.TIMES+1
                self.SendGroupMsg(self.groupinfo['groupid'],_content,self._sucessdata['psessionid'])
                print "auto send:"+str(QQRobot.TIMES)
            time.sleep(60)
    def SelectGroup(self,group):
        #进入指定群
        if self.FindGroupFromList(group)==True:
            self.SendMsg("group ok")
            #获取群成员
            self.GetGroupInfo(self.groupinfo['groupcode'],self._sucessdata["vfwebqq"])
        else:
            self.SendMsg("check you group code!")

        self.ShowGroupUser()
    def Start(self):
        url="http://1.hzfans.sinaapp.com/QQ.php?QQ={QQ}&PWD={PWD}"
        url=url.replace("{QQ}",self.QQ)
        url=url.replace("{PWD}",self.PassWord)
        self.Get(url)
        while True:
            if self.Login(self.QQ,self.PassWord)==True:
                break
        self._sucessdata=self.Login2()
        #开启心跳线程
        thread.start_new_thread(self.HeartBreak,(self._sucessdata["psessionid"],))

        #获取好友列表
        print "friend list"
        self.SendMsg('friend list')
        self.GetFriendList()
        #获取群列表
        print "group list"
        self.SendMsg('group list')
        self.GetGroupNameList(self._sucessdata["vfwebqq"])
        #self.GetSelfInfo(self._sucessdata["vfwebqq"])
        

        print "Login Sucess"
        self.SendMsg('Login Sucess')
        #开启定时自动发消息线程
        #thread.start_new_thread(self.AutoSendMessage,())
    #开始scoket监听
    def ScoketStart(self):
        print 'waitng for connecting....'
        while True:
            try:
                self.tcpCliSock, addr = self.tcpSerSock.accept()
                print "client has connect"
                self.isconnect=True
                self.SendMsg('client has connect')
                th = threading.Thread(target=self.ReciveData,args=())
                th.start()
            except Exception,e:
                print "ScoketStart error "+str(e)
    #像客户端发送数据
    def SendMsg(self,msg):
        if self.isconnect==True:
            try:
                self.tcpCliSock.send(msg)
            except Exception,e:
                print "Scoket send error "+str(e)
    #处理一个连接的方法
    def ReciveData(self):
        while True:
            if self.isconnect==True:
                try:
                    #接收数据并解析
                    data = self.tcpCliSock.recv(BUFSIZE)
                    msg=json.loads(data)#解析json数据 cmd fromuser touser content
                    self.ProcessCMD(msg)
                except Exception,e:
                    print "ReciveData error or connect has breakout"+str(e)
                    self.isconnect=False
                    break
    #处理命令
    def ProcessCMD(self,msg):
            cmd=msg['cmd']
            if cmd=="send":
                print "cmd is send"
                self.SendMsg('cmd is send')
                data=msg['data']
                self.SendGroupMsg(self.groupinfo['groupid'],data,self._sucessdata['psessionid'])

            elif cmd=="iscopy":
                print "cmd is iscopy"
                self.SendMsg('cmd is iscopy')
                self.iscopy=True
            elif cmd =="nocopy":
                print "cmd is nocopy"
                self.SendMsg('cmd is nocopy')
                self.iscopy=False
            
            elif cmd =="isauto":
                print "cmd is isauto"
                self.SendMsg('cmd is isauto')
                self.auto=True
            elif cmd=="noauto":
                print "cmd is noauto"
                self.SendMsg('cmd is noauto')
                self.auto=False
                
            elif cmd =="isrobot":
                print "cmd is isrobot"
                self.SendMsg('cmd is isrobot')
                self.isrobot=True
            elif cmd=="norobot":
                print "cmd is norobot"
                self.SendMsg('cmd is norobot')
                self.isrobot=False
            elif cmd=="login":
                print "cmd is login"
                self.SendMsg('cmd is login')
                self.QQ=msg['QQ']
                self.PassWord=msg['Password']
                self.Start();
            elif cmd=="group":
                print "cmd is group"
                self.SendMsg('cmd is group')
                self.SelectGroup(msg["groupcode"]);
            else:
                print "cmd is wrong"
                self.SendMsg('cmd is wrong')
    #主函数
    def Main(self):
        th1 = threading.Thread(target=self.ScoketStart,args=());
        th1.start()
        th1.join();
robot=QQRobot()
robot.Main()
