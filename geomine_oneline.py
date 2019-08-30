#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import makereq
import parser
import sys

# Changelog
# v1 03.11.2017 use parser.py

input_suggestion = "Sisesta programmi käsu järel aarde number, või täispikk link geopeituse aarde lehele:\ngeomine.py 3708\ngeomine.py \"http://www.geopeitus.ee/aare/3708\""


# Hangime kasutaja sisendi
try:
    sys.argv[1]
except Exception:
    print(input_suggestion)
    exit(0)
else:
    try:
        sys.argv[2]
    except Exception:
        if sys.argv[1].isdigit():
            print("Leidsime sisendi kujul: aarde number")
            aardelink = "http://www.geopeitus.ee/aare/" + str(sys.argv[1])
        elif str(sys.argv[1]).find("&c=") > 0:
            aardenumber = sys.argv[1].split("&c=")
            print(("DBG Leidsime sisendi kujul: " + str(aardenumber)))
            print(("DBG Leidsime sisendi kujul0: " + str(aardenumber[0])))
            print(("DBG Leidsime sisendi kujul1: " + str(aardenumber[1])))
            aardelink = "http://www.geopeitus.ee/aare/" + str(aardenumber[1])
        else:
            aardelink = str(sys.argv[1])
    else:
        print(("DBG Leidsime teise argumendi (" + str(sys.argv[2]) + ")...töötleme seda"))
        aardenumber = str(sys.argv[2]).ltrim("c=")
        print(("DBG Leidsime sisendi kujul: " + str(aardenumber)))
        aardelink = "http://www.geopeitus.ee/aare/" + str(aardenumber)


if len(aardelink) < len("http://www.geopeitus.ee/aare/") + 1:
    print(("Aadress: " + aardelink + " pole otsimiseks sobilik (liiga lühike)"))
    print(input_suggestion)
    exit(0)
else:
    aardenumber = parser.getNumFromUrl(aardelink)
    print(("Asume hankima andmeid aadressilt: " + aardelink + ""))

# hangime andmed
session=makereq.gpLogin()
cacheRaw = makereq.getCacheHtml(aardenumber, session)
cacheHtml = cacheRaw[1]
cacheLink = cacheRaw[0]
cacheData = parser.extractCacheInfo(cacheHtml, cacheLink, 10)

if (cacheData is None):
    exit(0)

# valime hangitud andmetest vajalikud väljad
nimi = cacheData['Name']
north = cacheData['Lat']
east = cacheData['Lon']
tyyp = cacheData['Type']
peidukoht = cacheData['Hide']
maastik = cacheData['Terrain']
suurus = cacheData['Size']
vihje = cacheData['Hint']
logid_types = cacheData['l_type']
logid_dates = cacheData['l_date']
leitud = 999

# koordinaadi konditsioneerimine
if tyyp == str("multi"):
    north = "A" + str(north)
    east = "A" + str(east)

elif tyyp == str("mõistatus"):
    north = "?" + str(north)
    east = "?" + str(east)

elif tyyp == str("Veebikaamera"):
    north = "CAM" + str(north)
    east = "CAM" + str(east)

elif tyyp == str("sündmus"):
    north = "EVENT" + str(north)
    east = "EVENT" + str(east)

elif tyyp == str("asukohata"):
    north = ""
    east = ""
else:
    north = str(north)
    east = str(east)

# viimase leidmisaja analüüs
for i in range(0, len(logid_types)):
    logi_type = logid_types[i]
    if(logi_type == "Found it"):
        logi_date = logid_dates[i]
        if logi_date is None:
            continue
        logi_date = str(logid_dates[i]).split(" ")[0]
        date_parts = logi_date.split("-")
        # kuupäeva muutmine: 0 1 2 -> 1 2 0
        leitud = date_parts[1] + str('/') + \
            date_parts[2] + str('/') + date_parts[0]
        break

tab = "\t"
newline = "\n"

# määrame printimisel kasutatava separaatori
sep = " \t"

print((newline +
       str(nimi) +
       sep +
       str(tyyp) +
       sep +
       str(peidukoht) +
       sep +
       str(maastik) +
       sep +
       str(suurus) +
       sep +
       str(north) +
       sep +
       str(east) +
       sep +
       str(leitud) +
       sep +
       str(vihje) +
       sep +
       str(aardelink) +
       newline
       ))
