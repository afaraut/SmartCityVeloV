import sqlite3
import time
import datetime
import numpy
from scipy import stats

def availableCyclicMean(type, stationId, thresholdMinutes, cursor):

	available, numberOfWeeks, availableCyclicMean  = list(), list(), list()

	if not type in ['bike','stand'] :
		print type
		return availableCyclicMean

	if type == 'bike':
		stationAvailabilityData = cursor.execute('SELECT timestamp, availableBikes FROM OldResults WHERE stationId =:stationId', { "stationId": stationId})
	if type == 'stand':
		stationAvailabilityData = cursor.execute('SELECT timestamp, availableStand FROM OldResults WHERE stationId =:stationId', { "stationId": stationId})

	indices = weekCycleIndices(thresholdMinutes)
	for indice in indices:
		numberOfWeeks.insert(indice, 0)
		available.insert(indice, 0)

	if stationAvailabilityData.rowcount == 0:
		print('unknown station with id : ' , stationId)


	for data in stationAvailabilityData:
		indice = timestampToWeekCycleIndice(data[0], thresholdMinutes)
		available[indice] += data[1]
		numberOfWeeks[indice] += 1

	for indice in indices:
		if numberOfWeeks[indice] == 0:
			availableCyclicMean.insert(indice,0)
		else:
			availableCyclicMean.insert(indice, round(float(available[indice])/numberOfWeeks[indice],2))

	return availableCyclicMean

def dailyCyclicMeans(cyclicMean, thresholdMinutes):
	dailyCyclicAmplitude = list()
	maxIndice = 24*7*60/thresholdMinutes

	for day in range(7):
		first = day*maxIndice/7
		last = (day+1)*maxIndice/7
		dailyCyclicAmplitude.insert(day,round(float(sum(cyclicMean[first:last])/len(cyclicMean[first:last])),2))

	return dailyCyclicAmplitude

def dayMeans(type, stationId, cursor):

	dayTotal, dayCount, dayMeans = dict(), dict(), dict()

	if not type in ['bike','stand'] :
		print type
		return dayMeans

	if type == 'bike':
		stationAvailabilityData = cursor.execute('SELECT timestamp, availableBikes FROM OldResults WHERE stationId =:stationId', { "stationId": stationId})
	if type == 'stand':
		stationAvailabilityData = cursor.execute('SELECT timestamp, availableStand FROM OldResults WHERE stationId =:stationId', { "stationId": stationId})

	for data in stationAvailabilityData:
		dayId = timestampToDayId(data[0])

		if dayId in dayTotal:
			dayTotal[dayId] = dayTotal[dayId] + data[1]
			dayCount[dayId] = dayCount[dayId] + 1
		else:
			dayTotal[dayId] = data[1]
			dayCount[dayId] = 1

	for dayId in dayTotal:
		if dayCount[dayId] > 0:
			dayMeans[dayId] = round(float(dayTotal[dayId])/dayCount[dayId],2)
		else:
			dayMeans[dayId] = 0

	return dayMeans

def stationName(stationId, cursor):
	return (cursor.execute('SELECT stationName FROM station WHERE id = :stationId', {"stationId" : stationId}).fetchone()[0])

def timestampToDayId(timestamp): #returns a unique day id with year-[1-366]
	dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	dayOfYear = (int(datetime.datetime.strftime(dateFromTimestamp,"%j"))) #between 1 and 366
	day = (int(datetime.datetime.strftime(dateFromTimestamp,"%d")))
	month = (int(datetime.datetime.strftime(dateFromTimestamp,"%m")))
	year = int(datetime.datetime.strftime(dateFromTimestamp,"%Y"))
	dayId = datetime.datetime(year,month,day)
	#print(dayId)
	return dayId


def weekCycleIndices(thresholdInMinutes):
	maxIndice = 24*7*60/thresholdInMinutes
	indices = list()
	for indice in range(maxIndice):
		indices.append(indice)
	return indices

def timestampToWeekCycleIndice(timestamp, thresholdInMinutes):
	dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	dayOfWeek = timestampToDayOfWeek(timestamp)
	hour = int(datetime.datetime.strftime(dateFromTimestamp,"%H"))
	minute = int(datetime.datetime.strftime(dateFromTimestamp,"%M"))
	minuteRound = minute - (minute % thresholdInMinutes)

	return dayOfWeek*24*60/thresholdInMinutes + hour*60/thresholdInMinutes + minuteRound/thresholdInMinutes


def timestampToDayOfWeek(timestamp):
	#in strftime sunday = 0, saturday = 6 -> convert to monday = 0, sunday = 6
	dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	return (int(datetime.datetime.strftime(dateFromTimestamp,"%w"))+6) % 7 

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


db = sqlite3.connect('../../data/velos')
cursor = db.cursor()

thresholdInMinutes = 5 # prevision precision threshlod in minutes
stationId = 9013

stationName = stationName(stationId,cursor)

print'station', stationId, stationName

cyclicL_bikes = availableCyclicMean('bike', stationId,thresholdInMinutes,cursor)
#print(bikes)
print "max available bikes: ", max(cyclicL_bikes)
print "min available bikes: ", min(cyclicL_bikes)
print "avg available bikes: ", round(float(sum(cyclicL_bikes))/len(cyclicL_bikes),2)

cyclicL_stands = availableCyclicMean('stand', stationId,thresholdInMinutes,cursor)
#print(stands)
print "max available stands: ", max(cyclicL_stands)
print "min available stands: ", min(cyclicL_stands)
print "avg available stands: ", round(float(sum(cyclicL_stands))/len(cyclicL_stands),2)

A_mod_d7_bikes = dailyCyclicMeans(cyclicL_bikes,thresholdInMinutes)
#print(A_mod_d7_bikes)
A_mod_d7_stands = dailyCyclicMeans(cyclicL_stands,thresholdInMinutes)
#print(A_mod_d7_stands)

A_d_d_bikes = dayMeans('bike', stationId, cursor)
A_d_d_stands = dayMeans('stand', stationId, cursor)
#print(A_d_d_bikes)
#print(A_d_d_stands)

L_mod_t_bikes, F = dict(), dict()

for data in cursor.execute('SELECT timestamp, availableBikes FROM OldResults WHERE stationId =:stationId', { "stationId": stationId}):
	timestamp = data[0]
	realAvailableBikes = data[1]
	dayOfWeek = timestampToDayOfWeek(timestamp)
	weekCycleIndice = timestampToWeekCycleIndice(timestamp, thresholdInMinutes)
	dayId = timestampToDayId(timestamp)
	#print timestamp, dayOfWeek, weekCycleIndice, dayId
	
	
	availableBikesPrevision = round(float(A_d_d_bikes[dayId]) * cyclicL_bikes[weekCycleIndice] / A_mod_d7_bikes[dayOfWeek],2)
	L_mod_t_bikes[timestamp] = availableBikesPrevision
	F[timestamp] = round(realAvailableBikes - availableBikesPrevision,2)
	#print availableBikesPrevision, realAvailableBikes

#print(F)

#regression Y(d7) = a * X(d7) + b
X , Y, Ycount = list(), list(), list()

for d7 in range(7):
	X.append(A_mod_d7_bikes[d7] - float(sum(A_mod_d7_bikes)/len(A_mod_d7_bikes)))
	# y = mean (A_d_d where d = d7)
	Y.insert(d7, 0)
	Ycount.insert(d7, 0)

for dayTimestamp in A_d_d_bikes:
	#dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	#print dayTimestamp
	d7 = dayTimestamp.isoweekday()-1
	#print d7
	Y[d7] = Y[d7] + A_d_d_bikes[dayTimestamp]
	Ycount[d7] = Ycount[d7] + 1

for d7 in range(7):
	Y[d7] = float(Y[d7]/Ycount[d7])

print X
print Y

c1, A0, r_value, p_value, std_err = stats.linregress(X,Y)
print 'a=', c1, "b=", A0
print "r-squared", r_value**2

A_d_d_bikes_minus_a0 = dict()
for dayTimestamp in A_d_d_bikes:
	d7 = dayTimestamp.isoweekday()-1
	a0 = A0 + c1 * X[d7] #use previous regression
	A_d_d_bikes_minus_a0[dayTimestamp] = A_d_d_bikes[dayTimestamp] - a0

#print(A_d_d_bikes_minus_a0)

weather_data = cursor.execute('SELECT * FROM weather')
temperatures, precipitations = list(), list()
#temperatureTotal, temperatureCount, precipitationTotal, precipitationCount = 0 , 0 , 0 , 0

for data in weather_data:
	if is_number(data[1]) :
		#temperatureTotal = temperatureTotal + float(data[1])
		#temperatureCount = temperatureCount + 1
		print data[0], data[1]
		temperatures.append(float(data[1]))
	
	if is_number(data[2]) :
		#precipitationTotal = precipitationTotal + float(data[2])
		#precipitationCount = precipitationCount + 1
		precipitations.append(float(data[2]))

tempMean = numpy.mean(temperatures)
tempStdDev = numpy.std(temperatures)
precStdDev = numpy.std(precipitations)

#print tempMean, tempStdDev, precStdDev

normalizedTemperatures, normalizedPrecipitations = dict(), dict()

for data2 in weather_data:
	if is_number(data2[1]) :
		#temperatureTotal = temperatureTotal + float(data2[1])
		#temperatureCount = temperatureCount + 1
		normalizedTemperatures[data2[0]] = (float(data2[1]) - tempMean ) / tempStdDev
	
	if is_number(data2[2]) :
		#precipitationTotal = precipitationTotal + float(data2[2])
		#precipitationCount = precipitationCount + 1
		normalizedPrecipitations[data2[0]] = float(data2[2]) / precStdDev

#print normalizedTemperatures

vacation = dict()

vacationData = cursor.execute('SELECT timestamp, vacation FROM OldResults WHERE stationId =:stationId', { "stationId": stationId})

for vacData in vacationData:
	dayId = timestampToDayId(data[0])
	vacation[dayId] = int(data[1])
	print int(data[1])


db.close()