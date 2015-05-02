#!/usr/local/bin/python
# -*- coding: utf-8	 -*-	
import codecs, os
import urllib2
import time
from time import gmtime, strftime
import json
import datetime
import sqlite3

db = sqlite3.connect('velos')
cursor = db.cursor()

while(True):
	response = urllib2.urlopen('https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json')
	html = response.read()
	data = json.loads(html)
	with codecs.open("./temp/last_update.csv", "w", "utf-8") as outfile:
		linetowrite =''
		cursor.execute('''DELETE FROM `RecentResults`''')
		for ligne in data['values']:

			data_date = ligne[18]
			data_stationId = ligne[0]
			data_status = ligne[11]
			data_availableBikes = ligne[12]
			data_availableStands = ligne[13]
			date = datetime.datetime.strptime(data_date, "%Y-%m-%d %H:%M:%S")
			data_day = datetime.datetime.strftime(date,"%A")
			data_hour = datetime.datetime.strftime(date,"%H")
			timestmp = int(time.mktime(datetime.datetime.strptime(data_date,"%Y-%m-%d %H:%M:%S").timetuple()))
			vacation = "NULL"

			f_jours = open('jours_feriesv2.txt')
			texte_f_jours = f_jours.readlines()
			jours = texte_f_jours[0].split(';')
			date_str = datetime.datetime.strftime(datetime.datetime.fromtimestamp(timestmp),"%d/%m/%y")
			if date_str in jours:
				vacation = 1

			linetowrite = data_stationId+'\t'+data_status+'\t'+str(timestmp)+'\t'+data_availableBikes+'\t'+data_availableStands
			cursor.execute('''INSERT INTO RecentResults(stationId, status, lastUpdate, availableBikes, availableStands)
              		    VALUES(?,?,?,?,?)''', (data_stationId,data_status,data_date,data_availableBikes,data_availableStands))
			cursor.execute("SELECT RecentResults.stationId, RecentResults.lastUpdate FROM RecentResults, OldResults WHERE RecentResults.stationId=OldResults.stationId AND OldResults.timestamp=:timestamp",{"timestamp":timestmp})
			if len(cursor.fetchall())==0:
				cursor.execute('''INSERT INTO OldResults(stationId, timestamp, dayOfWeek, hourOfDay, availableStand, availableBikes, vacation)
              			    VALUES(?,?,?,?,?,?,?)''', (data_stationId,timestmp,data_day,data_hour,data_availableStands,data_availableBikes,vacation))
			
			print linetowrite
			outfile.write(linetowrite)
	db.commit()
	time.sleep(60)
