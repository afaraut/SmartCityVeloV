import sqlite3
import time
import datetime
db = sqlite3.connect('velos')
cursor = db.cursor()
f = open('clean_v2.csv')
for line in f:	
	data = line.split(';')
	cursor.execute('''INSERT INTO OldResults(stationId, dayOfWeek, hourOfDay, timestamp, availableStand, availableBikes, vacation)
              		    VALUES(?,?,?,?,?,?,?)''', (data[0], data[3],data[2], data[1],data[4],data[5],'NULL'))
f = open('meteo.txt')
for line in f:	
	data = line.split(' ')
	timestmp = time.mktime(datetime.datetime.strptime(data[0]+'/'+data[1][0:2], "%d/%m/%Y/%H").timetuple())
	if len(data) == 4:
		cursor.execute('''INSERT INTO Weather(timestamp, temperatur, precipitation)
	              		    VALUES(?,?,?)''', (timestmp, data[2],data[3].split('\\')[0]))
	elif len(data) == 2:
		cursor.execute('''INSERT INTO Weather(timestamp, temperatur, precipitation)
	              		    VALUES(?,?,?)''', (timestmp, 'NULL','NULL'))
f = open('station_data.csv')
for line in f:	
	print line
	print line.decode('UTF-8')
	data = line.decode('UTF-8').split('\t')
	cursor.execute('''INSERT INTO Station(id, stationName, adress, totalBikes, longitude, latitude, bonus, banking)
              		    VALUES(?,?,?,?,?,?,?,?)''', (data[0], data[1],data[2] if data[3]=="None" else data[2]+', '+data[3],data[4], data[6],data[5],'NULL',data[7]))

f = open('meteo_jour.csv')
for line in f:	
	data = line.split(',')
	timestmp = time.mktime(datetime.datetime.strptime(data[0], "%d/%m/%Y").timetuple())

	cursor.execute('''INSERT INTO Weather_day(day, temperature, precipitation)
	              		VALUES(?,?,?)''', (timestmp, data[1],data[2]))

db.commit()
	