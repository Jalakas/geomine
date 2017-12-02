# coding=utf-8
from lxml import html,etree
from datetime import datetime
import makereq

#Funktsioon teisendab veebist loetud väärtused XML-i jaoks sobivaks
def valueMapper(parsedType, parsedValue):
   cacheType      = {"Tavaline aare" : "Traditional Cache",
                     "Mõistatusaare" : "Mystery Cache",
                     "Multiaare" : "Multi Cache"} 
   
   cacheArchived  = {"!!! Arhiveeritud !!!" : "True",
                     "!!! Ajutiselt kättesaamatu !!!" : "False",
                     "!!! Vajab hooldust !!!" : "False",
                     "" : "False"}
   
   cacheAvailable = {"!!! Arhiveeritud !!!" : "False",
                     "!!! Ajutiselt kättesaamatu !!!" : "False",
                     "!!! Vajab hooldust !!!":"True",
                     "" : "True"}
   
   cacheSize      = {"normaalne" : "Regular",
                     "mikro" : "Micro",
                     "väike" : "Small",
                     "suur" : "Large"}
   
   logType        = {"/ug/icons/emoticon_smile.png" : "Found it",
                     "/ug/icons/emoticon_unhappy2.png" : "Ei leidnud",
                     "/ug/icons/comment.png" : "Kommenteeris",
                     "/ug/icons/wrench_orange.png" : "Soovis hooldamist",
                     "/ug/icons/wrench.png" : "Hooldas",
                     "/ug/icons/exclamation.png" : "Soovis arhiveerimist"}
   
   if parsedType == "cacheAvailable":
      return list(map(cacheAvailable.get, parsedValue))
   elif parsedType == "cacheArchived":
      return list(map(cacheArchived.get, parsedValue))
   elif parsedType == "cacheType":
      return list(map(cacheType.get, parsedValue))
   elif parsedType == "cacheSize":
      return list(map(cacheSize.get, parsedValue))
   elif parsedType == "logType":
      return list(map(logType.get, parsedValue))
   else:
      return None

#Funktsioon parsib Xpathi järgi htmlist välja
def extractor(tree,xpath,n): #Xpath ja mitmes element massiivist
   try:
      if n is None:
         cacheProperty = str(tree.xpath(xpath)).lstrip('\r\n').rstrip('\r\n').lstrip(' ').rstrip(' ').encode(encoding='UTF-8',errors='ignore')
      else:
         cacheProperty = tree.xpath(xpath)[n].lstrip('\r\n').rstrip('\r\n').lstrip(' ').rstrip(' ').encode(encoding='UTF-8',errors='ignore')
   except:
      cacheProperty = ''
   return cacheProperty
   
#Funktsioon kontrollib, kas sisend on kuupäev   
def isValueDate(string,fmt):
   try: 
      l_time=datetime.strptime(string, fmt)
      return l_time
   except ValueError:
      return None

#Peameetod andmete lugemiseks HTML-ist
def extractCacheInfo(cacheHtml,link,logCount):
   tree=html.fromstring(cacheHtml)
   
   #Esmased töötlemata andmed
   cacheName   = extractor(tree,'//div[@class="cacheinfo"]/div/h1/text()',1)
   cacheLoc    = extractor(tree,'//div[@class="cacheinfo"]/table/tr[3]/td/b[1]/text()',0)
   cacheType   = extractor(tree,'//div[@class="cacheinfo"]/table/tr[5]/td/b[1]/text()',0)
   cacheDif    = extractor(tree,'//div[@class="cacheinfo"]/table/tr[6]/td/text()',0)
   cacheSize   = extractor(tree,'//div[@class="cacheinfo"]/table/tr[6]/td/text()',1)
   cacheStatus = extractor(tree,'//div[@class="cacheinfo"]/div/h1[2]/font/text()',0)
   cacheHint   = extractor(tree,'//span[@id="cachehint"]/text()',0) or '-'
   cachePlaced = extractor(tree,'//div[@class="cacheinfo"]/div/p/text()',0)
   cachePlBy   = extractor(tree,'//div[@class="cacheinfo"]/div/p/a/text()',0) or '-'
   cacheState  = extractor(tree,'//div[@class="cacheinfo"]/table/tr[5]/td/b[2]/text()',0)
   
   cacheDesc   = ''
   for elem in tree.xpath('//div[@class="cache-description"]'):
      cacheDesc = cacheDesc + etree.tostring(elem, pretty_print=True)

   logIds      = tree.xpath('//div[@class="eventlog"]/a[1]/@name')[:logCount]
   logFinders  = tree.xpath('//div[@class="eventlog"]/b[2]/text()')
   logFinders  = map(lambda x: x.encode(encoding='UTF-8',errors='ignore'), logFinders[:logCount])
   logTypes    = valueMapper('logType',tree.xpath('//div[@class="eventlog"]/a[1]/img[1]/@src'))[:logCount]
   logDates    = tree.xpath('//div[@class="eventlog"]/a[1]/@title')[:logCount]
   logDates    = map(lambda x: isValueDate(x[-19:],'%d.%m.%Y %H:%M:%S'),logDates)
   logTexts0   = tree.xpath('//div[@class="eventlog"]')[:logCount]
   logTexts    = []

   for i,elem in enumerate(logTexts0,1):
      logTexts.append(''.join(tree.xpath('//div[@class="eventlog"]['+str(i)+']/p/text()')))
   logTexts  = map(lambda x: x.encode(encoding='UTF-8',errors='ignore'), logTexts)
   cacheID     = link[link.rfind('/')+1:]

   #Töödeldud andmed
   cacheLocN   = cacheLoc[:9].replace(',','.')
   cacheLocE   = cacheLoc[10:].replace(',','.')
   cacheHid    = cacheDif[10:14]
   cacheTerr   = cacheDif[23:] 
   cachePlDt   = cachePlaced[7:17]
   cachePlBy   = cachePlaced[18:(cachePlaced.index('[')-1)] or '?'
   cacheOwner  = cachePlaced[cachePlaced.index('[')+1:cachePlaced.index(']')] 
   
   #Lisamappingut vajavad andmed
   cacheAvail  = valueMapper('cacheAvailable', [cacheStatus])[0]
   cacheArch   = valueMapper('cacheArchived', [cacheStatus])[0]
   cacheType   = valueMapper('cacheType', [cacheType])[0]
   cacheSize   = valueMapper('cacheSize', [cacheSize])[0]

   i=0
   cacheDescFormatted = ''
   while i < len(cacheDesc):
      cacheDescFormatted = cacheDescFormatted + cacheDesc[i]
      i+=1
      
   cacheData   = {'Name'   : cacheName, 
                  'Lat'    : cacheLocN,
                  'Lon'    : cacheLocE,
                  'Type'   : cacheType,
                  'Hide'   : cacheHid,
                  'Terrain': cacheTerr,
                  'Size'   : cacheSize,
                  'Desc'   : cacheDesc,
                  'Hint'   : cacheHint,
                  'Avail'  : cacheAvail,
                  'Arch'   : cacheArch,
                  'Owner'  : cacheOwner,
                  'PlDt'   : cachePlDt,
                  'PlBy'   : cachePlBy,
                  'State'  : cacheState,
                  'ID'     : cacheID,
                  'Link'   : link,
                  'l_id'   : logIds,
                  'l_find' : logFinders,
                  'l_type' : logTypes,
                  'l_date' : logDates,
                  'l_text' : logTexts}
   return cacheData
