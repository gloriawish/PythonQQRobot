#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#http://www.weather.com.cn/data/sk/101010100.html         实时
#http://www.weather.com.cn/data/cityinfo/101010100.html   全天
#http://m.weather.com.cn/data/101010100.html     六天

##http://www.google.com/ig/api?weather=Beijing 英文
##http://www.google.com/ig/api?weather=TOKYO
##http://www.google.com/ig/api?weather=Beijing&hl=zh-cn 中文

import os, io, sys, re, time, base64, json
import webbrowser, urllib2,urllib
import cookielib
from urllib import quote
from urllib import unquote

cj = cookielib.LWPCookieJar() 
cookie_support = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
urllib2.install_opener(opener)
class Tool():
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
            print e
            return None
    def Post(self,url,data,Host=None,Referer=None,Origin=None):
        try:
            postData = urllib.urlencode(data)
            #postData = data
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
            print e
            return None
    #北上广深
    cityList_bsgs = [
        {'code':"101010100", 'name':"北京"},
        {'code':"101020100", 'name':"上海"},
        {'code':"101280101", 'name':"广州"},
        {'code':"101280601", 'name':"深圳"}
    ]

    cityList_main = [   #全国主要城市
        #华北
        {'code':"101010100", 'name':"北京"},
        {'code':"101030100", 'name':"天津"},
        {'code':"101090101", 'name':"石家庄"},
        {'code':"101100101", 'name':"太原"},
        {'code':"101080101", 'name':"呼和浩特"},
        {'code':"101090201", 'name':"保定"},
        {'code':"101100201", 'name':"大同"},
        {'code':"101080201", 'name':"包头"},
        {'code':"101090402", 'name':"承德市"},
        {'code':"101100401", 'name':"晋中"},
        {'code':"101080501", 'name':"通辽"},
        {'code':"101091101", 'name':"秦皇岛"},
        #东北
        {'code':"101050101", 'name':"哈尔滨"},
        {'code':"101060101", 'name':"长春"},
        {'code':"101070101", 'name':"沈阳"},
        {'code':"101050201", 'name':"齐齐哈尔"},
        {'code':"101060201", 'name':"吉林"},
        {'code':"101070201", 'name':"大连"},
        {'code':"101050301", 'name':"牡丹江"},
        {'code':"101060301", 'name':"延吉"},
        {'code':"101070301", 'name':"鞍山"},
        {'code':"101050501", 'name':"绥化"},
        {'code':"101060601", 'name':"白城"},
        {'code':"101071401", 'name':"葫芦岛"},
        #华南
        {'code':"101280101", 'name':"广州"},
        {'code':"101300101", 'name':"南宁"},
        {'code':"101310101", 'name':"海口"},
        {'code':"101320101", 'name':"香港"},
        {'code':"101330101", 'name':"澳门"},
        {'code':"101280601", 'name':"深圳"},
        {'code':"101300501", 'name':"桂林"},
        {'code':"101310201", 'name':"三亚"},
        {'code':"101280701", 'name':"珠海"},
        {'code':"101281701", 'name':"中山"},
        {'code':"101301001", 'name':"百色"},
        {'code':"101310215", 'name':"万宁"},
        #西北
        {'code':"101110101", 'name':"西安"},
        {'code':"101160101", 'name':"兰州"},
        {'code':"101150101", 'name':"西宁"},
        {'code':"101170101", 'name':"银川"},
        {'code':"101130101", 'name':"乌鲁木齐"},
        {'code':"101110300", 'name':"延安"},
        {'code':"101110901", 'name':"宝鸡"},
        {'code':"101160901", 'name':"天水"},
        {'code':"101170301", 'name':"吴忠"},
        {'code':"101130501", 'name':"吐鲁番"},
        {'code':"101160801", 'name':"酒泉"},
        {'code':"101170401", 'name':"固原"},
        #西南
        {'code':"101040100", 'name':"重庆"},
        {'code':"101270101", 'name':"成都"},
        {'code':"101260101", 'name':"贵阳"},
        {'code':"101290101", 'name':"昆明"},
        {'code':"101140101", 'name':"拉萨"},
        {'code':"101270401", 'name':"绵阳"},
        {'code':"101260201", 'name':"遵义"},
        {'code':"101290201", 'name':"大理"},
        {'code':"101271401", 'name':"乐山"},
        {'code':"101260801", 'name':"六盘水"},
        {'code':"101291401", 'name':"丽江"},
        #华东
        {'code':"101020100", 'name':"上海"},
        {'code':"101230101", 'name':"福州"},
        {'code':"101220101", 'name':"合肥"},
        {'code':"101240101", 'name':"南昌"},
        {'code':"101120101", 'name':"济南"},
        {'code':"101210301", 'name':"嘉兴"},
        {'code':"101190101", 'name':"南京"},
        {'code':"101210401", 'name':"宁波"},
        {'code':"101210101", 'name':"杭州"},
        {'code':"101190401", 'name':"苏州"},
        {'code':"101120201", 'name':"青岛"},
        {'code':"101230201", 'name':"厦门"},
        {'code':"101340101", 'name':"台北市"},
        #华中
        {'code':"101180101", 'name':"郑州"},
        {'code':"101200101", 'name':"武汉"},
        {'code':"101250101", 'name':"长沙"},
        {'code':"101180201", 'name':"安阳"},
        {'code':"101200201", 'name':"襄阳"},
        {'code':"101250201", 'name':"湘潭"},
        {'code':"101250301", 'name':"株洲"},
        {'code':"101180401", 'name':"许昌"},
        {'code':"101250601", 'name':"常德"},
        {'code':"101251101", 'name':"张家界"},
        {'code':"101200401", 'name':"孝感"},
        {'code':"101201401", 'name':"荆门"}
    ]

    #返回dict类型: twitter = {'image': imgPath, 'message': content}
    def getCityWeather_RealTime(self,cityID):
        url = "http://www.weather.com.cn/data/sk/" + str(cityID) + ".html"
        try:
            stdout = urllib2.urlopen(url)
            weatherInfomation = stdout.read().decode('utf-8')

            jsonDatas = json.loads(weatherInfomation)

            city        = jsonDatas["weatherinfo"]["city"]
            temp        = jsonDatas["weatherinfo"]["temp"]
            fx          = jsonDatas["weatherinfo"]["WD"]        #风向
            fl          = jsonDatas["weatherinfo"]["WS"]        #风力
            sd          = jsonDatas["weatherinfo"]["SD"]        #相对湿度
            tm          = jsonDatas["weatherinfo"]["time"]

            content = u"#" + city + u"#" + u" " + temp + u"℃ " + fx + fl + u" " + u"相对湿度" + sd + u" "  + u"发布时间:" + tm
            twitter = {'image': "", 'message': content}

        except Exception,e:
            print e
        else:
            return twitter
        finally:
            None

    #返回dict类型: twitter = {'image': imgPath, 'message': content}
    def getCityWeatherDetail_SixDay(self,cityID):
        url = "http://m.weather.com.cn/data/" + str(cityID) + ".html"
        try:
            stdout = urllib2.urlopen(url)
            weatherInfomation = stdout.read().decode('utf-8')
            jsonDatas = json.loads(weatherInfomation)

            city        = jsonDatas["weatherinfo"]["city"]
            tempF1      = jsonDatas["weatherinfo"]["tempF1"]
            weather     = jsonDatas["weatherinfo"]["img_title1"]
            img         = jsonDatas["weatherinfo"]["img1"]
            fx          = jsonDatas["weatherinfo"]["fx1"]       #风向
            cy            = jsonDatas["weatherinfo"]["index"]        #暖        #穿衣指数
            zw            = jsonDatas["weatherinfo"]["index_uv"]        #最弱   #紫外线指数
            xc            = jsonDatas["weatherinfo"]["index_xc"]        #不宜     #洗车
            tr            = jsonDatas["weatherinfo"]["index_tr"]        #很适宜    #旅游
            co            = jsonDatas["weatherinfo"]["index_co"]        #舒适     #舒适度
            cl            = jsonDatas["weatherinfo"]["index_cl"]        #较适宜  #晨练指数
            ls            = jsonDatas["weatherinfo"]["index_ls"]        #不太适宜  #晾晒指数
            ag            = jsonDatas["weatherinfo"]["index_ag"]        #不易发"    #过敏
            temp1       = jsonDatas["weatherinfo"]["temp1"]
            temp2       = jsonDatas["weatherinfo"]["temp2"]
            temp3       = jsonDatas["weatherinfo"]["temp3"]
            temp4       = jsonDatas["weatherinfo"]["temp4"]
            temp5       = jsonDatas["weatherinfo"]["temp5"]
            temp6       = jsonDatas["weatherinfo"]["temp6"]
            weather1    = jsonDatas["weatherinfo"]["weather1"]
            weather2    = jsonDatas["weatherinfo"]["weather2"]
            weather3    = jsonDatas["weatherinfo"]["weather3"]
            weather4    = jsonDatas["weatherinfo"]["weather4"]
            weather5    = jsonDatas["weatherinfo"]["weather5"]
            weather6    = jsonDatas["weatherinfo"]["weather6"]

            if int(img) < 10:
                imgPath = "icon\d" + "0" + str(img) + ".gif"
            else:
                imgPath = "icon\d"       + str(img) + ".gif"

            content = u"#" + city + u"#" + u"\n<指数> " + u"穿衣:" + cy + u" 紫外线:" + zw + u" 洗车:" + xc \
                    + u" 旅游:" + tr + u" 舒适度:" + co + u" 晨练:" + cl + u" 晾晒:" + ls + u" 过敏:" + ag + u"\n" \
                    + u"<天气>" + u" 1天:" + temp1 + u" " + weather1 + u" 2天:" + temp2 + u" " + weather2  + u" 3天:" + temp3 + u" " + weather3\
                    + u" 4天:" + temp4 + u" " + weather4 + u" 5天:" + temp5 + u" " + weather5  + u" 6天:" + temp6 + u" " + weather6

            twitter = {'image': imgPath, 'message': content}

        except Exception,e:
            print e
        else:
            return twitter
        finally:
            None

    #返回dict类型: twitter = {'image': imgPath, 'message': content}
    def getCityWeather_AllDay(self,cityID):
        url = "http://www.weather.com.cn/data/cityinfo/" + str(cityID) + ".html"
        try:
            stdout = urllib2.urlopen(url)
            weatherInfomation = stdout.read().decode('utf-8')
            jsonDatas = json.loads(weatherInfomation)

            city        = jsonDatas["weatherinfo"]["city"]
            temp1       = jsonDatas["weatherinfo"]["temp1"]
            temp2       = jsonDatas["weatherinfo"]["temp2"]
            weather     = jsonDatas["weatherinfo"]["weather"]
            img1        = jsonDatas["weatherinfo"]["img1"]
            img2        = jsonDatas["weatherinfo"]["img2"]
            ptime        = jsonDatas["weatherinfo"]["ptime"]

            content = city + u"," + weather + u",最高气温:" + temp1 + u",最低气温:"  + temp2 + u",发布时间:" + ptime
            twitter = {'image': "icon\d" + img1, 'message': content}

        except Exception,e:
            print e
        else:
            return twitter
        finally:
            None
    def getCityCodeFromName(self,cityName):  
        for item in Tool.cityList_main:  
           city=unicode(item['name'],'utf-8')
           if city.strip()==cityName.strip():
               return item['code']
    def convertName(self,cityName):  
        #将 “浙江省杭州市” 转换成“杭州”   
        #print 'convertName:',cityName  
        try:
            name = unicode(cityName, "utf8")
        except Exception,e:
            name = cityName 
        if name.find(u"省") !=-1:# 包含'省'   
            #print u'有省'  
            name=name.split(u'省')[1]  
        if name.find(u"市") != -1:#包含‘市’  
            #print u'有市'  
            name=name.split(u'市')[0]  
        return name
    def GetWeather(self,city):
        cityName=self.convertName(city) 
        cityID=self.getCityCodeFromName(cityName)
        twitter=self.getCityWeather_AllDay(cityID)
        if twitter==None:
            return
        return twitter["message"]
    def AutoAnswer(self,question):
        question=quote(question.encode('utf8'))
        url="http://xiao.douqq.com/api.php?msg={$question}&type=json"
        url=url.replace("{$question}",question)
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        message=resp.read()
        jsonret=json.loads(message)
        return jsonret["msg"]
    def xiaodou(self,qustion):
        url="http://xiao.douqq.com/bot/chat.php"
        qustion=quote(qustion.encode('utf8'))
        data="chat={chat}"
        data=data.replace("{chat}",qustion)
        req = urllib2.Request(url, data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
        req.add_header('Accept', '*/*')
        #req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        req.add_header('Connection', 'keep-alive')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_header('Host', 'xiao.douqq.com')
        req.add_header('Referer', 'http://xiao.douqq.com/')
        req.add_header('Origin', 'http://xiao.douqq.com')
        
        response = urllib2.urlopen(req)
        the_page = response.read()
        
        return the_page
        

def GetWeather(city):
    w=Tool()
    return w.GetWeather(city)

def GetAutoAnswer(question):
    w=Tool()
    return w.xiaodou(question)
