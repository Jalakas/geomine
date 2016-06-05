# coding=utf-8
from lxml import html,etree

def valueMapper(parsedtype, parsedvalue):
	cacheType 		= {"Tavaline aare" : "Traditional Cache",
							"Mõistatusaare" : "Mystery Cache",
							"Multiaare" : "Multi Cache"} 
	
	cacheArchived	= {"!!! Arhiveeritud !!!" : "True",
							"!!! Ajutiselt kättesaamatu !!!" : "False"}
	
	cacheAvailable = {"!!! Arhiveeritud !!!" : "False",
							"!!! Ajutiselt kättesaamatu !!!" : "False"}
	
	cacheSize		= {"normaalne" : "Regular",
							"mikro" : "Micro",
							"väike" : "Small",
							"suur" : "Large"}
	
	if parsedtype == "cacheAvailable":
		try:
			return cacheAvailable[parsedvalue.encode(encoding='UTF-8')]
		except:
			return None
	elif parsedtype == "cacheArchived":
		try:
			return cacheArchived[parsedvalue.encode(encoding='UTF-8')]
		except:
			return None
	elif parsedtype == "cacheType":
		try:
			return cacheType[parsedvalue.encode(encoding='UTF-8')]
		except:
			return None
	elif parsedtype == "cacheSize":
		try:
			return cacheSize[parsedvalue.encode(encoding='UTF-8')]
		except:
			return None

#Funktsioon parsib Xpathi järgi htmlist välja
def extractor(tree,xpath,n): #Xpath ja mitmes element massiivist
	try:
		if n is None:
			cacheProperty = str(tree.xpath(xpath)).lstrip('\r\n').rstrip('\r\n').lstrip(' ').rstrip(' ')
		else:
			cacheProperty = tree.xpath(xpath)[n].lstrip('\r\n').rstrip('\r\n').lstrip(' ').rstrip(' ')
	except:
		cacheProperty = ''
	return cacheProperty


def extractCacheInfo(cacheHtml,link):
	tree=html.fromstring(cacheHtml)
	
	#Esmased andmed
	cacheName	= extractor(tree,'//div[@class="cacheinfo"]/div/h1/text()',1)
	cacheLoc		= extractor(tree,'//div[@class="cacheinfo"]/table/tr[3]/td/b[1]/text()',0)
	cacheType	= extractor(tree,'//div[@class="cacheinfo"]/table/tr[5]/td/b[1]/text()',0)
	cacheDif		= extractor(tree,'//div[@class="cacheinfo"]/table/tr[6]/td/text()',0)
	cacheSize	= extractor(tree,'//div[@class="cacheinfo"]/table/tr[6]/td/text()',1)
	cacheStatus	= extractor(tree,'//div[@class="cacheinfo"]/div/h1[2]/font/text()',0)
	cacheHint	= extractor(tree,'//span[@id="cachehint"]/text()',0)
	cachePlaced	= extractor(tree,'//div[@class="cacheinfo"]/div/p/text()',0)
	cacheState	= extractor(tree,'//div[@class="cacheinfo"]/table/tr[5]/td/b[2]/text()',0)
	
	cacheDesc	= ''
	for elem in tree.xpath('//div[@class="cache-description"]'):
		cacheDesc = cacheDesc + etree.tostring(elem, pretty_print=True)
	
	cacheID		= link[link.rfind('/'):]
	print(cacheID)
	
	#Töödeldud andmed
	cacheLocN	= cacheLoc[:9].replace(',','.')
	cacheLocE	= cacheLoc[10:].replace(',','.')
	cacheHid		= cacheDif[10:14]
	cacheTerr	= cacheDif[23:]
	cachePlDt	= cachePlaced[7:17]
	cachePlBy	= cachePlaced[18:(cachePlaced.index('[')-1)]
	cacheOwner	= cachePlaced[cachePlaced.index('[')+1:cachePlaced.index(']')]

	#Lisamappingut vajavad andmedelem
	cacheAvail	= valueMapper('cacheAvailable', cacheStatus)
	cacheArch	= valueMapper('cacheArchived', cacheStatus)
	cacheType	= valueMapper('cacheType', cacheType)
	cacheSize	= valueMapper('cacheSize', cacheSize)

	i=0
	cacheDescFormatted = ''
	while i < len(cacheDesc):
		cacheDescFormatted = cacheDescFormatted + cacheDesc[i]
		i+=1
		
	cacheData 	= {'Name'	: cacheName, 
						'Lat'		: cacheLocN,
						'Lon'		: cacheLocE,
						'Type'	: cacheType,
						'Hide'	: cacheHid,
						'Terrain': cacheTerr,
						'Size'	: cacheSize,
						'Desc'	: cacheDesc,
						'Hint'	: cacheHint,
						'Avail'	: cacheAvail,
						'Arch'	: cacheArch,
						'Owner'	: cacheOwner,
						'PlDt'	: cachePlDt,
						'PlBy'	: cachePlBy,
						'State'	: cacheState}
	return cacheData

