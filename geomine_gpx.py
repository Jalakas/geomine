#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Geopeitus.ee aardeinfo Garmin GPX formaati salvestamiseks"""
import makereq
import parser
import gpxmaker
import sys


global version
version = '0.3.1'

print(('### Geopeitus.ee GPX failide koostaja v:' + version + ' ###'))
print('-----------------------------------------')
if sys.version_info[0] != 3:
    print('   VIGA! Toetatud on ainult Python 3!')
    sys.exit(0)

if sys.version_info[1] != 6:
    print('   Hoiatus! Ei ole Python 3.6. Programm ei pruugi töötada korrektselt!')


while True:
    print('   Sisesta link või aarde number: ')
    inStr = sys.stdin.readline(100).strip()
    if inStr == 'exit':
        break
    cacheNum = parser.getNumFromUrl(inStr)

    if cacheNum is None:
        print('   Arusaamatu sisend!\n   Sisesta aare kujul \'1043\' või \'http://www.geopeitus.ee/aare/1043\'')
        continue
    cacheRaw = makereq.getCacheHtml(cacheNum)
    cacheHtml = cacheRaw[1]
    cacheLink = cacheRaw[0]

    cachedata = parser.extractCacheInfo(cacheHtml, cacheLink, 15)
    gpx = gpxmaker.makeGpx(cachedata)

    try:
        gpx.write(open('GP' + str(cacheNum) + '.gpx', 'wb'),
                  encoding='UTF-8', pretty_print=True)
        print(('   Aardeinfo salvestatud: ' + 'GP' + str(cacheNum) + '.gpx'))
    except BaseException:
        print('   Viga! - Ei õnnestunud faili salvestada!')
