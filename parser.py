#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Geopeitus.ee aardelehelt aardeinfo väljalugemiseks ja teisendamiseks
    Groundspeak GPX formaadile vastavateks väärtusteks
"""

from lxml import etree
from lxml import html
from datetime import datetime


def getNumFromUrl(inStr):
    """Funktsioon tagastab URL-i põhjal aarde ID"""

    cache_id = ''
    if len(inStr) >= 0 and len(inStr) <= 4:
        try:
            cache_id = int(inStr)
        except BaseException:
            print('   Sisestatu pole aarde number')
            return None
    if len(inStr) > 4:
        try:
            search_str = 'geopeitus.ee/aare/'
            cache_index = inStr.find(search_str)
            if cache_index >= 0:
                cache_id = int(inStr[(cache_index + len(search_str)):])
            else:
                print('   Tundmatu link')
                return None
        except BaseException:
            print('   Tundmatu link')
            return None
    return cache_id


def valueMapper(parsedType, parsedValue):
    """Funktsioon teisendab veebist loetud väärtused XML-i jaoks sobivaks"""

    cacheType = {"Tavaline aare": "Traditional Cache",
                 "Mõistatusaare": "Mystery Cache",
                 "Multiaare": "Multi Cache",
                 "Sündmusaare": "Unknown Cache"}

    cacheArchived = {"!!! Arhiveeritud !!!": "True",
                     "!!! Ajutiselt kättesaamatu !!!": "False",
                     "!!! Vajab hooldust !!!": "False",
                     "": "False"}

    cacheAvailable = {"!!! Arhiveeritud !!!": "False",
                      "!!! Ajutiselt kättesaamatu !!!": "False",
                      "!!! Vajab hooldust !!!": "True",
                      "": "True"}

    cacheSize = {"normaalne": "Regular",
                 "mikro": "Micro",
                 "väike": "Small",
                 "suur": "Large"}

    logType = {"/ug/icons/emoticon_smile.png": "Found it",
               "/ug/icons/emoticon_unhappy2.png": "Didn't find it",
               "/ug/icons/comment.png": "Write note",
               "/ug/icons/wrench_orange.png": "Needs Maintenance",
               "/ug/icons/wrench.png": "Owner Maintenance",
               "/ug/icons/exclamation.png": "Temporarily Disable Listing"}

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


def isValueDate(string, fmt):
    """Funktsioon kontrollib, kas sõne on kuupäev"""
    try:
        l_time = datetime.strptime(string, fmt)
        return l_time
    except ValueError:
        return None


def extractCacheInfo(cacheHtml, link, logCount=10):
    """Peameetod andmete lugemiseks ja parsimiseks HTML-ist"""

    if(cacheHtml == b'<pre>DB Error: syntax error'):
        print('Parser: Vigane sisend! (sellise lingi peal pole aaret?)')
        return None

    tree = html.fromstring(cacheHtml)

    # Aarde nimi
    cacheName = tree.xpath('//div[@class="cacheinfo"]/div/h1/text()')[1].lstrip('\r\n').rstrip('\r\n')

    # Aarde koordinaadid
    cacheLoc = tree.xpath('//div[@class="cacheinfo"]/table/tr[3]/td/b[1]/text()')[0]
    cacheLocN = cacheLoc[:9].replace(',', '.').lstrip(' ')
    cacheLocE = cacheLoc[10:].replace(',', '.').lstrip(' ')

    # Aarde tüüp
    cacheType = tree.xpath('//div[@class="cacheinfo"]/table/tr[5]/td/b[1]/text()')[0]
    cacheType = valueMapper('cacheType', [cacheType])[0]

    # Aarde keerukus ja maastik
    cacheDif = tree.xpath('//div[@class="cacheinfo"]/table/tr[6]/td/text()')[0]
    cacheHid = cacheDif[10:14].lstrip(' ').rstrip(' ')
    cacheTerr = cacheDif[23:].lstrip(' ').rstrip(' ')

    # Aarde suurus
    cacheSize = tree.xpath('//div[@class="cacheinfo"]/table/tr[6]/td/text()')[1]
    cacheSize = cacheSize.lstrip(' ')
    cacheSize = valueMapper('cacheSize', [cacheSize])[0]

    # Aarde saadavus / staatus
    cacheStatus = list(tree.xpath('//div[@class="cacheinfo"]/div/h1[2]/font/text()') or '')
    cacheAvail = 'True'
    cacheArch = 'False'
    if len(cacheStatus) > 0:
        cacheAvail = ''.join(valueMapper('cacheAvailable', [cacheStatus[0]]))
        cacheArch = ''.join(valueMapper('cacheArchived', [cacheStatus[0]]))

    # Aarde vihje
    cacheHint = tree.xpath('//span[@id="cachehint"]/text()')
    if len(cacheHint) > 1:
        cacheHint = ''.join(cacheHint).replace('\r\n', ' ')
    elif len(cacheHint) == 1:
        cacheHint = cacheHint[0]
    else:
        cacheHint = '-'

    # Aarde peitja info
    cachePlaced = tree.xpath('//div[@class="cacheinfo"]/div/p/text()')[0]
    cachePlDt = isValueDate(cachePlaced[7:17], '%d.%m.%Y')
    cachePlBy = cachePlaced[18:(cachePlaced.index('[') - 1)] or '?'
    cacheOwner = cachePlaced[cachePlaced.index('[') + 1:cachePlaced.index(']')]

    # Aarde maakond
    cacheState = tree.xpath('//div[@class="cacheinfo"]/table/tr[5]/td/b[2]/text()')[0]

    # Aarde kirjeldus HTML vormingus
    cacheDesc = str('')
    for elem in tree.xpath('//div[@class="cache-description"]'):
        cacheDesc = cacheDesc + str(etree.tostring(elem), 'ascii').rstrip('\r\n')

    # Aarde kirjeldus tekstina
    cacheDescNoTags = str('')
    cacheDescNoTags = ''.join(html.fromstring(cacheDesc).itertext())

    # Logide ID väärtused
    logIds = tree.xpath('//div[@class="eventlog"]/a[1]/@name')[:logCount]

    # Logide autorid
    logFinders0 = tree.xpath('//div[@class="eventlog"]/b[2]/text()')
    logFinders = logFinders0[:logCount]

    # Logide tüübid
    logTypes = valueMapper('logType', tree.xpath(
        '//div[@class="eventlog"]/a[1]/img[1]/@src'))[:logCount]

    # Logide kuupäevad
    logDates = tree.xpath('//div[@class="eventlog"]/a[1]/@title')[:logCount]
    logDates = list([isValueDate(
        x[-19:], '%d.%m.%Y %H:%M:%S') for x in logDates])

    # Logide tekstid
    logTexts = []

    for i, elem in enumerate(tree.xpath('//div[@class="eventlog"]')[:logCount], 1):
        logTexts.append(
            ''.join(
                tree.xpath('//div[@class="eventlog"][' + str(i) + ']/p/text()')))

    # Aarde ID väärtus
    cacheID = link[link.rfind('/') + 1:]

    cacheData = {'Name': cacheName,
                 'Lat': cacheLocN,
                 'Lon': cacheLocE,
                 'Type': cacheType,
                 'Hide': cacheHid,
                 'Terrain': cacheTerr,
                 'Size': cacheSize,
                 'Desc': cacheDesc,
                 'DescPlain': cacheDescNoTags,
                 'Hint': cacheHint,
                 'Avail': cacheAvail,
                 'Arch': cacheArch,
                 'Owner': cacheOwner,
                 'PlDt': cachePlDt,
                 'PlBy': cachePlBy,
                 'State': cacheState,
                 'ID': cacheID,
                 'Link': link,
                 'l_id': logIds,
                 'l_find': logFinders,
                 'l_type': logTypes,
                 'l_date': logDates,
                 'l_text': logTexts}
                 
    return cacheData
