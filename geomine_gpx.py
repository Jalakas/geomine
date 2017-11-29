# coding=utf-8
import makereq
import parser
import gpxmaker
import sys

def getUrlAndNum(inStr):
   cache_id = ''
   if len(inStr) >= 0 and len(inStr) <=4:
      try: 
         cache_id    = int(inStr)
      except:
         print('   Sisestatu pole aarde number')
         return None
   if len(inStr)>4:
      try:
         search_str  = 'geopeitus.ee/aare/'
         cache_index = inStr.find(search_str)
         if cache_index >= 0:
            cache_id = int(inStr[(cache_index+len(search_str)):])
         else:
            print('   Tundmatu link')
            return None
      except:
         print('   Tundmatu link')
         return None
   return cache_id

print('### Geopeitus.ee GPX failide koostaja ###')
while True:
   print('Sisesta link või aarde number: ')
   inStr = sys.stdin.readline(100).strip()
   if inStr == 'exit':
      break
   cacheNum=getUrlAndNum(inStr)
   
   if cacheNum == None:
      print('   Arusaamatu sisend!\n   Sisesta aare kujul \'1043\' või \'http://www.geopeitus.ee/aare/1043\'')
      continue
   cacheRaw=makereq.getCacheHtml(cacheNum)
   cacheHtml=cacheRaw[1]
   cacheLink=cacheRaw[0]

   cachedata=parser.extractCacheInfo(cacheHtml,cacheLink)
   gpx=gpxmaker.makeGpx(cachedata)

   try:
      fw = open('GP'+str(cacheNum)+'.gpx','w')
      fw.write(gpx)
      fw.close
      print('Aardeinfo salvestatud: '+'GP'+str(cacheNum)+'.gpx')
   except:
      print('Viga! - Ei õnnestunud faili salvestada!')

