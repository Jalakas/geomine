# coding=utf-8
from lxml import etree
from lxml.builder import ElementMaker
from time import strftime, gmtime

def makeGpx(cachedata):

   #XML namespace and header
   XMLSchInst        = "http://www.w3.org/2001/XMLSchema-instance"
   XSLSchInst        = "http://www.w3.org/2001/XMLSchema"
   schemaLocation    = "http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0 http://www.groundspeak.com/cache/1/0/cache.xsd" 
   XML_NS            = "http://www.topografix.com/GPX/1/0"
   gs                = "groundspeak"
   gsurl             = "http://www.groundspeak.com/cache/1/0"
   
   version="1.0"
   creator="Geomine"
   
   NS_MAP = {"xsi": XMLSchInst,
             "xsd": XSLSchInst,
              None: XML_NS}
   
   
   #XML struktuur
   root              = etree.Element("gpx", version=version, attrib={"{"+XMLSchInst+"}schemaLocation" : schemaLocation}, creator=creator, nsmap=NS_MAP)
   name              = etree.SubElement(root, "name")
   desc              = etree.SubElement(root, "desc")
   author            = etree.SubElement(root, "author")
   email             = etree.SubElement(root, "email")
   url               = etree.SubElement(root, "url")
   urlname           = etree.SubElement(root, "urlname")
   time              = etree.SubElement(root, "time")
   keywords          = etree.SubElement(root, "keywords")
   bounds            = etree.SubElement(root, "bounds")
   wpt               = etree.SubElement(root, "wpt")
   
   wpt_time          = etree.SubElement(wpt, "time")
   wpt_name          = etree.SubElement(wpt, "name")        
   wpt_desc          = etree.SubElement(wpt, "desc")
   wpt_url           = etree.SubElement(wpt, "url")
   wpt_urlname       = etree.SubElement(wpt, "urlname")
   wpt_sym           = etree.SubElement(wpt, "sym")
   wpt_type          = etree.SubElement(wpt, "type")
   
   gs_cache          = etree.SubElement(wpt, "{"+gsurl+"}cache", nsmap={gs: gsurl})
   gs_name           = etree.SubElement(gs_cache,"{"+gsurl+"}name")
   gs_placed_by      = etree.SubElement(gs_cache,"{"+gsurl+"}placed_by") 
   gs_owner          = etree.SubElement(gs_cache,"{"+gsurl+"}owner")
   gs_type           = etree.SubElement(gs_cache,"{"+gsurl+"}type")
   gs_container      = etree.SubElement(gs_cache,"{"+gsurl+"}container")
   gs_difficulty     = etree.SubElement(gs_cache,"{"+gsurl+"}difficulty")
   gs_terrain        = etree.SubElement(gs_cache,"{"+gsurl+"}terrain")
   gs_country        = etree.SubElement(gs_cache,"{"+gsurl+"}country")
   gs_state          = etree.SubElement(gs_cache,"{"+gsurl+"}state")
   gs_short_desc     = etree.SubElement(gs_cache,"{"+gsurl+"}short_description")
   gs_long_desc      = etree.SubElement(gs_cache,"{"+gsurl+"}long_description")
   gs_encoded_hints  = etree.SubElement(gs_cache,"{"+gsurl+"}encoded_hints")
   gs_logs           = etree.SubElement(gs_cache,"{"+gsurl+"}logs")
   
   #Make input text XML-compatible
   for key, value in cachedata.items():
      cachedata[key]=map(lambda x: x.decode(encoding='UTF-8',errors='ignore').encode('ascii','xmlcharrefreplace'),value)
         
   #Fill the XML
   name.text               = "Geopeituse aare"
   desc.text               = "Aardeinfo Geopeitus.ee lehelt"
   author.text             = ""
   email.text              = ""
   url.text                = "http://www.geopeitus.ee"
   urlname.text            = "Geopeitus.ee"
   time.text               = strftime("%Y-%m-%d%a%H:%M:%S", gmtime())
   keywords.text           = "cache, geocache"
   bounds.attrib['minlat'] = ''.join(cachedata['Lat'])
   bounds.attrib['minlon'] = ''.join(cachedata['Lon'])
   bounds.attrib['maxlat'] = ''.join(cachedata['Lat'])
   bounds.attrib['maxlon'] = ''.join(cachedata['Lon'])
   
   wpt.attrib['lat']       = ''.join(cachedata['Lat'])
   wpt.attrib['lon']       = ''.join(cachedata['Lon'])
   wpt_time.text           = ''.join(cachedata['PlDt'])
   wpt_name.text           = "GP"+''.join(cachedata['ID'])
   wpt_desc.text           = ''.join(cachedata['Name']) + ' Peitja: '+''.join(cachedata['PlBy'])+' '+ ''.join(cachedata['Type']) +' ('+ ''.join(cachedata['Hide']) + '/' + ''.join(cachedata['Terrain']) + ')' 
   wpt_url.text            = ''.join(cachedata['Link'])
   wpt_urlname.text        = 'GP - '+''.join(cachedata['Name'])
   wpt_sym.text            = 'Geocache'
   wpt_type.text           = 'Geocache|'+''.join(cachedata['Type'])
   
   gs_cache.attrib['id']         = ''.join(cachedata['ID'])
   gs_cache.attrib['available']  = ''.join(cachedata['Avail'])
   gs_cache.attrib['archived']   = ''.join(cachedata['Arch'])
   
   gs_name.text            = ''.join(cachedata['Name'])
   gs_placed_by.text       = ''.join(cachedata['PlBy'])
   gs_owner.text           = ''.join(cachedata['Owner'])
   gs_type.text            = ''.join(cachedata['Type'])
   gs_container.text       = ''.join(cachedata['Size'])
   gs_difficulty.text      = ''.join(cachedata['Hide'])
   gs_terrain.text         = ''.join(cachedata['Terrain'])
   gs_country.text         = "Eesti"
   gs_state.text           = ''.join(cachedata['State'])
   gs_long_desc.text       = ''.join(cachedata['Desc'])
   gs_encoded_hints.text   = ''.join(cachedata['Hint'])
   
   #Logs
   i=0
   while i<len(cachedata['l_id']):
      logs_log       = etree.SubElement(gs_logs,"{"+gsurl+"}log")
      logs_log.attrib['id'] = cachedata['l_id'][i]
      
      log_date       = etree.SubElement(logs_log,"{"+gsurl+"}date")
      log_date.text  = cachedata['l_date'][i]
      
      log_type       = etree.SubElement(logs_log,"{"+gsurl+"}type")
      log_type.text  = cachedata['l_type'][i]
      
      log_finder     = etree.SubElement(logs_log,"{"+gsurl+"}finder")
      log_finder.text= cachedata['l_find'][i]    
       
      log_text       = etree.SubElement(logs_log,"{"+gsurl+"}text")
      log_text.text  = cachedata['l_text'][i]  
            
      i+=1

   return(etree.ElementTree(root))
