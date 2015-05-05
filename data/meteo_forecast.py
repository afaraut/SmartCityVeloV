#!/usr/local/bin/python

import codecs, os
import urllib
import urllib2
from urllib2 import Request
import time
from time import gmtime, strftime
import json
import datetime
import sqlite3

db = sqlite3.connect('velos',timeout=30.0)
cursor = db.cursor()

answer = False
while answer==False:
	try:
		f = urllib2.urlopen("http://api.openweathermap.org/data/2.5/forecast?q=Lyon&mode=json")
		answer = True
	except:
		time.sleep(5)
		answer = False

precipitation = -1
temperature = -1000
timestamp = 0
try:
	data = json.loads(f.read())
	print data.keys()
except:
	print "error while loading json"

cursor.execute('''DELETE FROM WeatherForecast''')
for X in range(0,len(data['list'])):
	try:
		#print data['list'][X]
		precipitation = data['list'][X]['rain']['3h']
		temperature = int(data['list'][X]['main']['temp'])-273.15
		timestamp = data['list'][X]['dt']
	except KeyError:
		try:
			precipitation = 0
			timestamp = data['list'][X]['dt']
			temperature = int(data['list'][X]['main']['temp'])-273.15
		except KeyError:
			print 'something went wrong with the weather api !'
	
	cursor.execute('''INSERT INTO WeatherForecast(timestamp, temperatur, precipitation)
	         		    VALUES(?,?,?)''', (timestamp,temperature,precipitation))
	print X, 'Resultat : timestamp :', timestamp, ' precipitation :', precipitation,' temperature: ', temperature

db.commit()