#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
import urllib2

def getNextTramTime():
    response = urllib2.urlopen('http://www.tam-voyages.com/horaires_arret/index.asp?rub_code=28&lign_id=1&sens=1&pa_id=1137')
    html = response.read()

    soup = BeautifulSoup(html,"html5lib")

    hours = []
    res = []

    for p in soup.find_all('thead'):
        for p in soup.find_all('tr'):
            for d in p.find_all('th'):
                hours.append(d.text)

    for p in soup.find_all('tbody'):
        for p in soup.find_all('tr'):
            tmp = p.find_all('td')
            for i in xrange(0,len(tmp)):
                for t in tmp[i].find_all('div'):
                    if not(t.text[0:2] == ""):
                        res.append(time.strptime(hours[i][0:2] + " " + t.text[0:2], "%H %M"))

    currentHour = time.localtime().tm_hour
    currentMinutes = time.localtime().tm_min

    print "Current time : ",currentHour, "h",currentMinutes,"min"

    for v in res:
        if currentHour < v.tm_hour or (currentHour == v.tm_hour and currentMinutes < v.tm_min):
            print "Next at : " + str(v.tm_hour), "h", str(v.tm_min), "min"
            return "%d h %d min" % (v.tm_hour, v.tm_min )
            break
