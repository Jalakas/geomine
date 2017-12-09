#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Groundspeak GPX formaadile vastava XML-i loomine"""
from lxml import etree
from time import gmtime
from time import strftime


def makeGpx(cachedata):
    """Groundspeak GPX formaadile vastava XML-i loomine"""

    # XML namespace and header
    XMLSchInst = "http://www.w3.org/2001/XMLSchema-instance"
    XSLSchInst = "http://www.w3.org/2001/XMLSchema"
    schemaLocation = "http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0 http://www.groundspeak.com/cache/1/0/cache.xsd"
    XML_NS = "http://www.topografix.com/GPX/1/0"
    gs = "groundspeak"
    gsurl = "http://www.groundspeak.com/cache/1/0"

    version = "2.0"
    creator = "Geomine"

    NS_MAP = {"xsi": XMLSchInst,
              "xsd": XSLSchInst,
              None: XML_NS}

    # XML struktuur
    root = etree.Element(
        "gpx",
        version=version,
        attrib={
            "{" + XMLSchInst + "}schemaLocation": schemaLocation},
        creator=creator,
        nsmap=NS_MAP)
    name = etree.SubElement(root, "name")
    desc = etree.SubElement(root, "desc")
    author = etree.SubElement(root, "author")
    email = etree.SubElement(root, "email")
    url = etree.SubElement(root, "url")
    urlname = etree.SubElement(root, "urlname")
    time = etree.SubElement(root, "time")
    keywords = etree.SubElement(root, "keywords")
    bounds = etree.SubElement(root, "bounds")
    wpt = etree.SubElement(root, "wpt")

    wpt_time = etree.SubElement(wpt, "time")
    wpt_name = etree.SubElement(wpt, "name")
    wpt_desc = etree.SubElement(wpt, "desc")
    wpt_url = etree.SubElement(wpt, "url")
    wpt_urlname = etree.SubElement(wpt, "urlname")
    wpt_sym = etree.SubElement(wpt, "sym")
    wpt_type = etree.SubElement(wpt, "type")

    gs_cache = etree.SubElement(wpt, "{" + gsurl + "}cache", nsmap={gs: gsurl})
    gs_name = etree.SubElement(gs_cache, "{" + gsurl + "}name")
    gs_placed_by = etree.SubElement(gs_cache, "{" + gsurl + "}placed_by")
    gs_owner = etree.SubElement(gs_cache, "{" + gsurl + "}owner")
    gs_type = etree.SubElement(gs_cache, "{" + gsurl + "}type")
    gs_container = etree.SubElement(gs_cache, "{" + gsurl + "}container")
    gs_difficulty = etree.SubElement(gs_cache, "{" + gsurl + "}difficulty")
    gs_terrain = etree.SubElement(gs_cache, "{" + gsurl + "}terrain")
    gs_country = etree.SubElement(gs_cache, "{" + gsurl + "}country")
    gs_state = etree.SubElement(gs_cache, "{" + gsurl + "}state")
    gs_long_desc = etree.SubElement(
        gs_cache, "{" + gsurl + "}long_description")
    gs_encoded_hints = etree.SubElement(
        gs_cache, "{" + gsurl + "}encoded_hints")
    gs_logs = etree.SubElement(gs_cache, "{" + gsurl + "}logs")

    # XML-i elementide väärtustamine
    name.text = "Geopeituse aare"
    desc.text = "Aardeinfo Geopeitus.ee lehelt"
    author.text = ""
    email.text = ""
    url.text = "http://www.geopeitus.ee"
    urlname.text = "Geopeitus.ee"
    time.text = strftime("%Y-%m-%d%a%H:%M:%S", gmtime())
    keywords.text = "cache, geocache"
    bounds.attrib['minlat'] = cachedata['Lat']
    bounds.attrib['minlon'] = cachedata['Lon']
    bounds.attrib['maxlat'] = cachedata['Lat']
    bounds.attrib['maxlon'] = cachedata['Lon']

    wpt.attrib['lat'] = cachedata['Lat']
    wpt.attrib['lon'] = cachedata['Lon']
    wpt_time.text = cachedata['PlDt'].strftime("%Y-%m-%dT%H:%M:%S")
    wpt_name.text = "GP" + str(cachedata['ID'])
    wpt_desc.text = (str(cachedata['Name']) + ' Peitja: ' + str(cachedata['PlBy']) + ' ' + str(
        cachedata['Type']) + ' (' + str(cachedata['Hide']) + '/' + str(cachedata['Terrain']) + ')').encode('ascii', 'xmlcharrefreplace')
    wpt_url.text = str(cachedata['Link'])
    wpt_urlname.text = ('GP - ' + cachedata['Name']).encode('ascii', 'xmlcharrefreplace')
    wpt_sym.text = 'Geocache'
    wpt_type.text = ('Geocache|' + cachedata['Type']).encode('ascii', 'xmlcharrefreplace')

    gs_cache.attrib['id'] = str(cachedata['ID'])
    gs_cache.attrib['available'] = str(cachedata['Avail'])
    gs_cache.attrib['archived'] = str(cachedata['Arch'])

    gs_name.text = str(cachedata['Name']).encode('ascii', 'xmlcharrefreplace')
    gs_placed_by.text = str(cachedata['PlBy']).encode('ascii', 'xmlcharrefreplace')
    gs_owner.text = str(cachedata['Owner']).encode('ascii', 'xmlcharrefreplace')
    gs_type.text = str(cachedata['Type']).encode('ascii', 'xmlcharrefreplace')
    gs_container.text = str(cachedata['Size']).encode('ascii', 'xmlcharrefreplace')
    gs_difficulty.text = str(cachedata['Hide']).encode('ascii', 'xmlcharrefreplace')
    gs_terrain.text = str(cachedata['Terrain']).encode('ascii', 'xmlcharrefreplace')
    gs_country.text = "Eesti"
    gs_state.text = str(cachedata['State']).encode('ascii', 'xmlcharrefreplace')
    gs_long_desc.text = str(cachedata['Desc']).encode('ascii', 'xmlcharrefreplace')
    gs_encoded_hints.text = str(cachedata['Hint']).encode('ascii', 'xmlcharrefreplace')

    # Logid
    i = 0

    for i in enumerate(cachedata['l_id']):
        logs_log = etree.SubElement(gs_logs, "{" + gsurl + "}log")
        logs_log.attrib['id'] = list(cachedata['l_id'])[i[0]].encode('ascii', 'xmlcharrefreplace')

        log_date = etree.SubElement(logs_log, "{" + gsurl + "}date")
        log_date.text = list(cachedata['l_date'])[i[0]].strftime("%Y-%m-%dT%H:%M:%S")

        log_type = etree.SubElement(logs_log, "{" + gsurl + "}type")
        log_type.text = list(cachedata['l_type'])[i[0]].encode('ascii', 'xmlcharrefreplace')

        log_finder = etree.SubElement(logs_log, "{" + gsurl + "}finder")
        log_finder.text = list(cachedata['l_find'])[i[0]].encode('ascii', 'xmlcharrefreplace')

        log_text = etree.SubElement(logs_log, "{" + gsurl + "}text")
        log_text.text = list(cachedata['l_text'])[i[0]].encode('ascii', 'xmlcharrefreplace')

    return(etree.ElementTree(root))
