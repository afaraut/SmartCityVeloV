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


db = sqlite3.connect('velos')
cursor = db.cursor()
f = urllib2.urlopen("http://api.openweathermap.org/data/2.5/find?q=Lyon")
precipitation = -1
temperature = -1000
timestamp = 0
try:
	data = json.loads(f.read())
	print data.keys()
	print data['list'][0]
	precipitation = data['list'][0]['rain']['3h']
	temperature = int(data['list'][0]['main']['temp'])-273.15
	timestamp = data['list'][0]['dt']
except KeyError:
	try:
		precipitation = 0
		timestamp = data['list'][0]['dt']
		temperature = int(data['list'][0]['main']['temp'])-273.15
	except KeyError:
		print 'something went wrong with the weather api !'

cursor.execute('''SELECT * FROM Weather WHERE timestamp=:timestamp ''',{"timestamp":timestamp})
if len(cursor.fetchall())==0 and timestamp!=0 and precipitation>=0 and temperature!=-1000:
	cursor.execute('''INSERT INTO Weather(timestamp, temperatur, precipitation)
          		    VALUES(?,?,?)''', (timestamp,temperature,precipitation))
else:
	print 'error : timestamp :', timestamp, ' precipitation :'
db.commit()

