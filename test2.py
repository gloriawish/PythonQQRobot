# -*- coding: utf-8 -*-

import json
import urllib
import urllib2

s="r=%7B%22clientid%22%3A%2257728685%22%2C%22psessionid%22%3A%228368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363000003ae700001bda036200a192126d0000000a406f6972703777576a716d000000288572c44c47163fc4010a1421c52b60f486e06e9eb97194f81acd02757193d400c10aa825cadbc33e%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid=57728685&psessionid=8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363000003ae700001bda036200a192126d0000000a406f6972703777576a716d000000288572c44c47163fc4010a1421c52b60f486e06e9eb97194f81acd02757193d400c10aa825cadbc33e"

def GetParams(clientid,psessionid):
    r={
      "clientid":str(clientid),
      "psessionid":str(psessionid),
      "key":0,
      "ids":[]
      }
    r=json.dumps(r)
    data = {
            "r":r,
            "psessionid":str(psessionid),
            "clientid":clientid,
        }
    postdata=urllib.urlencode(data)
    postdata=postdata.replace("+","")
    return postdata