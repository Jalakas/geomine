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
   bounds.attrib['minlat'] = cachedata['Lat'][0]
   bounds.attrib['minlon'] = cachedata['Lon'][0]
   bounds.attrib['maxlat'] = cachedata['Lat'][0]
   bounds.attrib['maxlon'] = cachedata['Lon'][0]
   
   wpt.attrib['lat']       = cachedata['Lat'][0]
   wpt.attrib['lon']       = cachedata['Lon'][0]
   wpt_time.text           = cachedata['PlDt'][0]
   wpt_name.text           = "GP"+cachedata['ID'][0]
   wpt_desc.text           = cachedata['Name'][0] + ' Peitja: '+cachedata['PlBy'][0]+' '+ cachedata['Type'][0] +' ('+ cachedata['Hide'][0] + '/' + cachedata['Terrain'][0] + ')' 
   wpt_url.text            = cachedata['Link'][0]
   wpt_urlname.text        = 'GP - '+cachedata['Name'][0]
   wpt_sym.text            = 'Geocache'
   wpt_type.text           = 'Geocache|'+cachedata['Type'][0]
   
   gs_cache.attrib['id']         = cachedata['ID'][0]
   gs_cache.attrib['available']  = cachedata['Avail'][0]
   gs_cache.attrib['archived']   = cachedata['Arch'][0]
   
   gs_name.text            = cachedata['Name'][0]
   gs_placed_by.text       = cachedata['PlBy'][0]
   gs_owner.text           = cachedata['Owner'][0]
   gs_type.text            = cachedata['Type'][0]
   gs_container.text       = cachedata['Size'][0]
   gs_difficulty.text      = cachedata['Hide'][0]
   gs_terrain.text         = cachedata['Terrain'][0]
   gs_country.text         = "Eesti"
   gs_state.text           = cachedata['State'][0]
   gs_long_desc.text       = cachedata['Desc'][0]
   gs_encoded_hints.text   = cachedata['Hint'][0]
   
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
