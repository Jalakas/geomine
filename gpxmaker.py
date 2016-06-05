# coding=utf-8
from lxml import etree
from lxml.builder import ElementMaker
from time import strftime, gmtime

def makeGpx(cachedata):

	#XML namespaces and header
	XMLSchInst			= "http://www.w3.org/2001/XMLSchema-instance"
	XSLSchInst			= "http://www.w3.org/2001/XMLSchema"
	schemaLocation		= "http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0 http://www.groundspeak.com/cache/1/0/cache.xsd" 
	XML_NS				= "http://www.topografix.com/GPX/1/0"
	gs						= "groundspeak"
	gsurl 		  		= "http://www.groundspeak.com/cache/1/0"
	
	version="1.0"
	creator="Geomine"
	
	NS_MAP = {"xsi": XMLSchInst,
				 "xsd": XSLSchInst,
				  None: XML_NS}
	
	
	#XML structure
	root        		= etree.Element("gpx", version=version, attrib={"{"+XMLSchInst+"}schemaLocation" : schemaLocation}, creator=creator, nsmap=NS_MAP)
	name        		= etree.SubElement(root, "name")
	desc        		= etree.SubElement(root, "desc")
	author      		= etree.SubElement(root, "author")
	email       		= etree.SubElement(root, "email")
	url 					= etree.SubElement(root, "url")
	urlname 				= etree.SubElement(root, "urlname")
	time 					= etree.SubElement(root, "time")
	keywords 			= etree.SubElement(root, "keywords")
	bounds 				= etree.SubElement(root, "bounds")
	wpt 					= etree.SubElement(root, "wpt")
	
	wpt_time				= etree.SubElement(wpt, "time")
	wpt_name				= etree.SubElement(wpt, "name")			
	wpt_desc				= etree.SubElement(wpt, "desc")
	wpt_url				= etree.SubElement(wpt, "url")
	wpt_urlname			= etree.SubElement(wpt, "urlname")
	wpt_sym				= etree.SubElement(wpt, "sym")
	wpt_type				= etree.SubElement(wpt, "type")
	
	gs_cache				= etree.SubElement(wpt, "{"+gsurl+"}cache", nsmap={gs: gsurl})
	gs_name				= etree.SubElement(gs_cache,"{"+gsurl+"}name")
	gs_placed_by		= etree.SubElement(gs_cache,"{"+gsurl+"}placed_by") 
	gs_owner				= etree.SubElement(gs_cache,"{"+gsurl+"}owner")
	gs_type				= etree.SubElement(gs_cache,"{"+gsurl+"}type")
	gs_container		= etree.SubElement(gs_cache,"{"+gsurl+"}container")
	gs_difficulty		= etree.SubElement(gs_cache,"{"+gsurl+"}difficulty")
	gs_terrain 			= etree.SubElement(gs_cache,"{"+gsurl+"}terrain")
	gs_country  		= etree.SubElement(gs_cache,"{"+gsurl+"}country")
	gs_state				= etree.SubElement(gs_cache,"{"+gsurl+"}state")
	gs_short_desc		= etree.SubElement(gs_cache,"{"+gsurl+"}short_description")
	gs_long_desc		= etree.SubElement(gs_cache,"{"+gsurl+"}long_description")
	gs_encoded_hints	= etree.SubElement(gs_cache,"{"+gsurl+"}encoded_hints")
	
	#Fill the XML
	name.text					= "Geopeituse aare"
	desc.text					= "Aardeinfo Geopeitus.ee lehelt"
	author.text					= ""
	email.text					= ""
	url.text						= "http://www.geopeitus.ee"
	urlname.text				= "Geopeitus.ee"
	time.text					= strftime("%Y-%m-%d%a%H:%M:%S", gmtime())
	keywords.text				= "cache, geocache"
	bounds.attrib['minlat']	= cachedata['Lat']
	bounds.attrib['minlon']	= cachedata['Lon']
	bounds.attrib['maxlat']	= cachedata['Lat']
	bounds.attrib['maxlon']	= cachedata['Lon']
	
	wpt.attrib['lat']			= cachedata['Lat']
	wpt.attrib['lon']			= cachedata['Lon']
	wpt_time.text				= cachedata['PlDt']
	wpt_name.text 				= "GP-"+cachedata['Name']
	wpt_desc.text 				= cachedata['Name'] + ' Peitja: '+cachedata['PlBy']+' '+ cachedata['Type'] +' ('+ cachedata['Hide'] + '/' + cachedata['Terrain'] + ')' 
	wpt_url.text				= 'Geopeituse aarde link' #TODO
	wpt_urlname.text			= 'GP - '+cachedata['Name']
	wpt_sym.text				= 'Geocache'
	wpt_type.text				= 'Geocache|'+cachedata['Type']
	
	gs_name.text				= cachedata['Name']
	gs_placed_by.text			= cachedata['PlBy']
	gs_owner.text				= cachedata['Owner']
	gs_type.text				= cachedata['Type']
	gs_container.text			= cachedata['Size']
	gs_difficulty.text		= cachedata['Hide']
	gs_terrain.text			= cachedata['Terrain']
	gs_country.text			= "Eesti"
	gs_state.text				= cachedata['State']
	gs_long_desc.text			= cachedata['Desc']
	gs_encoded_hints.text	= cachedata['Hint']

	return(etree.tostring(root,pretty_print=True, xml_declaration=True, encoding='UTF-8'))
