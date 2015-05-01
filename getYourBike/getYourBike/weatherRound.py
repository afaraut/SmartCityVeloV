import sqlite3
import util

def getNearestWeatherPastForRegression(F, hourLimit, db_path):
	db = sqlite3.connect(db_path)
	cursor = db.cursor()
	R, toRemove = dict(), list()
	for time in F:
		min_time = time-3600*hourLimit
		data = cursor.execute('''SELECT timestamp, precipitation FROM Weather WHERE timestamp>:lowLimit AND timestamp<=:highLimit ORDER BY timestamp DESC''',{"lowLimit":min_time, "highLimit":time}).fetchone()
		if data is None:
			toRemove.append(int(time))
		elif not util.is_number(data[1]):
			toRemove.append(int(time))
		else:
			R[int(time)] = float(data[1])
	return [R, toRemove]

def getNearestPrecipitationsForPrevision(times, hourLimit, db_path):
	db = sqlite3.connect(db_path)
	cursor = db.cursor()

	R = dict()

	for t in times:
		min_time = t-3600*hourLimit
		data = cursor.execute('''SELECT timestamp, precipitation FROM Weather WHERE timestamp>:lowLimit AND timestamp<=:highLimit ORDER BY timestamp DESC''',{"lowLimit":min_time, "highLimit":t}).fetchone()
		if data is None:
			R[t] = None
		elif not util.is_number(data[1]):
			R[t] = None
		else:
			R[t] = float(data[1])

	return R