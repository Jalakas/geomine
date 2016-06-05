# coding=utf-8
import requests

def makeReq(link):
   headers     = {
      'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
      'Accept-Encoding': 'gzip, deflate, compress'
   }
   session     = requests.session()
   req         = session.get( link ,   headers=headers)
   return req

def getCacheHtml(cachenum):
   return(["http://www.geopeitus.ee/aare/"+str(cachenum),makeReq("http://www.geopeitus.ee/aare/"+str(cachenum)).content])


