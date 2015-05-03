import codecs, os, urllib2, sqlite3, time, datetime

f = open('jours_feriesv2.txt')
texte = f.readlines()
jours = texte[0].split(';')
#print jours

db = sqlite3.connect('velos')
cursor = db.cursor()
cursor.execute('''SELECT DISTINCT stationId from OldResults''')
print cursor.rowcount
stations = [item[0] for item in cursor.fetchall()]
#print stations

for station in stations:
    cursor.execute("SELECT timestamp from OldResults WHERE stationId=? AND vacation='NULL'", [station])
    timestamps = [item[0] for item in cursor.fetchall()]
    for timestamp in timestamps:
        date = datetime.datetime.strftime(datetime.datetime.fromtimestamp(timestamp),"%d/%m/%y")
        if date in jours:
            param = [(station,),(timestamp,)]
            cursor.execute('UPDATE OldResults SET vacation =:val WHERE (stationId =:stat AND timestamp =:time)', {"val": 1,"stat":station, "time":timestamp})
db.commit()
	