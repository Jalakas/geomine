#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HTML-i hankimine"""
import requests
import getpass
import sys


def makeReq(link, session):
    """Päringu teostamine html-i allalaadimiseks"""
    req = session.get(link)
    return req


def getCacheHtml(cachenum, session):
    """Aarde ID järgi URL-i moodustamine"""
    return(["http://www.geopeitus.ee/aare/" + str(cachenum), makeReq("http://www.geopeitus.ee/aare/" + str(cachenum), session).content])
    
    
def gpLogin():
    """Enne esimest päringut logime sisse, et koordinaate näha"""
    print('Sisesta kasutajanimi:')
    gpUser = sys.stdin.readline(100).strip()
    gpPw = getpass.getpass(prompt='Parool')

    headers = {
        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Accept-Encoding': 'gzip, deflate, compress'}   
    loginData = {'LoginForm[username]': gpUser, 'LoginForm[password]': gpPw, 'uri':'/'}
    url = 'http://www.geopeitus.ee/site/login'
    
    session = requests.session()
    req = session.post(url, headers=headers, data=loginData)    
    return session
    #TODO kontrolli, kas login õnnestus
    
    
    
