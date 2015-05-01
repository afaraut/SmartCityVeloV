import sqlite3
import time
import datetime
import numpy
from scipy import stats
import timeit

import multilinearRegression
import weatherRound
import util



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

def fluctuationThresholdMeans(F):

	F_total, F_count, F_means = dict(), dict(), dict()

	for t in F:
		tRoundToThreshold = timestampRoundToThreshold(t)

		if tRoundToThreshold in F_total:
			F_total[tRoundToThreshold] = F_total[tRoundToThreshold]  + F[t]
			F_count[tRoundToThreshold] = F_count[tRoundToThreshold] + 1
		else:
			F_total[tRoundToThreshold] = F[t]
			F_count[tRoundToThreshold] = 1

	for tRound in F_total:

		tRoundInt = int(tRound)
		if F_count[tRound] > 0:
			F_means[tRoundInt] = round(float(F_total[tRound])/F_count[tRound],2)
		else:
			F_means[tRoundInt] = 0

	return F_means




def stationName(stationId):
	db = sqlite3.connect(db_path)
	cursor = db.cursor()
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

def timestampRoundToThreshold(timestamp):
	dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	#dayOfYear = (int(datetime.datetime.strftime(dateFromTimestamp,"%j"))) #between 1 and 366
	day = (int(datetime.datetime.strftime(dateFromTimestamp,"%d")))
	month = (int(datetime.datetime.strftime(dateFromTimestamp,"%m")))
	year = int(datetime.datetime.strftime(dateFromTimestamp,"%Y"))
	hour = int(datetime.datetime.strftime(dateFromTimestamp,"%H"))
	minute = int(datetime.datetime.strftime(dateFromTimestamp,"%M"))
	
	minuteRoundToThreshold = minute - (minute % thresholdInMinutes)
	datetimeRoundToThreshold = datetime.datetime(year, month, day, hour, minuteRoundToThreshold)

	return util.datetimeToTimestamp(datetimeRoundToThreshold)

def weekCycleIndices(thresholdInMinutes):
	maxIndice = 24*7*60/thresholdInMinutes
	indices = list()
	for indice in range(maxIndice):
		indices.append(indice)
	return indices

def timestampToWeekCycleIndice(timestamp, thresholdInMinutes):
	dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	dayOfWeek = util.timestampToDayOfWeek(timestamp)
	hour = int(datetime.datetime.strftime(dateFromTimestamp,"%H"))
	minute = int(datetime.datetime.strftime(dateFromTimestamp,"%M"))
	minuteRound = minute - (minute % thresholdInMinutes)

	return dayOfWeek*24*60/thresholdInMinutes + hour*60/thresholdInMinutes + minuteRound/thresholdInMinutes

def a0Regression(A_mod_d7_bikes, A_d_d_bikes):
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

	#print X
	#print Y

	c1, A0, r_value, p_value, std_err = stats.linregress(X,Y)
	#print 'a=', c1, "b=", A0
	#print "r-squared", r_value**2
	return [c1, A0, X]

def a0Prevision(timestamp, A0, c1, AmodDifferenceD7):
	d7 = timestampToDayId(timestamp).isoweekday()-1
	a0 = A0 + c1 * AmodDifferenceD7[d7]
	return a0


def getVacationData():
	vacation = dict()
	vacationRequest = cursor.execute('SELECT timestamp, vacation FROM OldResults WHERE stationId =:stationId', { "stationId": stationId}).fetchall()
	timestamps = [item[0] for item in vacationRequest]
	vacationData = [item[1] for item in vacationRequest]

	for index, vacData in enumerate(vacationData):
		dayId = timestampToDayId(timestamps[index])
		if vacData == 'NULL':
			vacData = '0'
		vacation[dayId] = int(vacData)

	return vacation

def getDailyWeatherData():
	weather_data = cursor.execute('SELECT * FROM weather_day').fetchall()
	temperatures, precipitations = list(), list()
	#temperatureTotal, temperatureCount, precipitationTotal, precipitationCount = 0 , 0 , 0 , 0

	for data in weather_data:
		if util.is_number(data[1]) :
			#temperatureTotal = temperatureTotal + float(data[1])
			#temperatureCount = temperatureCount + 1
			temperatures.append(float(data[1]))
		
		if util.is_number(data[2]) :
			#precipitationTotal = precipitationTotal + float(data[2])
			#precipitationCount = precipitationCount + 1
			precipitations.append(float(data[2]))

	tempMean = numpy.mean(temperatures)
	tempStdDev = numpy.std(temperatures)
	precStdDev = numpy.std(precipitations)

	#print tempMean, tempStdDev, precStdDev

	normalizedTemperatures, normalizedPrecipitations = dict(), dict()

	for data2 in weather_data:
		if util.is_number(data2[1]) :
			#temperatureTotal = temperatureTotal + float(data2[1])
			#temperatureCount = temperatureCount + 1
			dayId = timestampToDayId(data2[0])
			normalizedTemperatures[dayId] = (float(data2[1]) - tempMean ) / tempStdDev
		
		if util.is_number(data2[2]) :
			#precipitationTotal = precipitationTotal + float(data2[2])
			#precipitationCount = precipitationCount + 1
			dayId = timestampToDayId(data2[0])
			normalizedPrecipitations[dayId] = float(data2[2]) / precStdDev

	return [tempMean, tempStdDev, precStdDev, normalizedTemperatures, normalizedPrecipitations]

def L_mod_t_and_F(stationId, cyclicL, A_mod_d7, A_d_d):

	L_mod_t, F = dict(), dict()

	for data in cursor.execute('SELECT timestamp, availableBikes FROM OldResults WHERE stationId =:stationId', { "stationId": stationId}):
		timestamp = data[0]
		realAvailable = data[1]
		dayOfWeek = util.timestampToDayOfWeek(timestamp)
		weekCycleIndice = timestampToWeekCycleIndice(timestamp, thresholdInMinutes)
		dayId = timestampToDayId(timestamp)
		#print timestamp, dayOfWeek, weekCycleIndice, dayId
		
		
		availablePrevision = round(float(A_d_d[dayId]) * cyclicL[weekCycleIndice] / A_mod_d7[dayOfWeek],2)
		L_mod_t[timestamp] = availablePrevision
		F[timestamp] = round(realAvailable - availablePrevision,2)
		#print availableBikesPrevision, realAvailableBikes
	return [L_mod_t, F]

def substract_a0_from_Ad(c1, A0, AmodDifferenceD7, A_d_d):
	A_d_d_minus_a0 = dict()
	for dayTimestamp in A_d_d:
		d7 = dayTimestamp.isoweekday()-1
		a0 = A0 + c1 * AmodDifferenceD7[d7] #use previous regression
		A_d_d_minus_a0[dayTimestamp] = A_d_d[dayTimestamp] - a0
	return A_d_d_minus_a0


def prepareDataForDailyRegression(A_d_d_minus_a0, normalizedTemperatures, normalizedPrecipitations, vacation):
	toRemove = list()

	for d in A_d_d_minus_a0:
		#if (not d in normalizedTemperatures or not d in normalizedPrecipitations or not d in vacation):
			#toRemove.append(d)
			#print 'removed data', d
		if not d in normalizedTemperatures:
			toRemove.append(d)
			#print 'removed data (not present in normalizedTemperatures)', d
		elif not d in normalizedPrecipitations:
			toRemove.append(d)
			#print 'removed data (not present in normalizedPrecipitations)', d
		elif not d in vacation:
			toRemove.append(d)
			#print 'removed data (not present in vacation)', d

	for dToRemove in toRemove:
		#print 'removed data', d
		del A_d_d_minus_a0[dToRemove]

	x1, x2, x3, y = list(), list(), list(), list()

	for d2 in A_d_d_minus_a0:
		y.append(A_d_d_minus_a0[d2])
		x1.append(normalizedTemperatures[d2])
		x2.append(normalizedPrecipitations[d2])
		x3.append(vacation[d2])

	x = [x1, x2, x3]

	return [y, x]

def L_mod_prevision(timestamp, cyclicL, A_mod_d7, A0, c1, AmodDifferenceD7, C1, C2, C3, K, normalizedDeltaT, normalizedPrecipitations, V):

	dayOfWeek = util.timestampToDayOfWeek(timestamp)
	weekCycleIndice = timestampToWeekCycleIndice(timestamp, thresholdInMinutes)
	dayId = timestampToDayId(timestamp)
	a0 = float(a0Prevision(timestamp, A0, c1, AmodDifferenceD7))
	A_d_d_prevision = a0 + C1 * normalizedDeltaT + C2 * normalizedPrecipitations + C3 * V + K
	L_mod_prevision =  A_d_d_prevision * cyclicL[weekCycleIndice] / A_mod_d7[dayOfWeek]
	return round(L_mod_prevision,2)

def prepareDataForFluctuationRegression(F_threshold, weatherValidityHours):

	Fy_regression, Fx_regression, R_regression = list(), list(), list()
	[R, toRemove] = weatherRound.getNearestWeatherPastForRegression(F_threshold, weatherValidityHours, db_path)
	
	for rem in toRemove:
		del F_threshold[rem]
	
	sorted_t = sorted(F_threshold.keys())
	
	for t in sorted_t:
		previous_t = t - 60 * thresholdInMinutes
		if previous_t in F_threshold:
			Fy_regression.append(F_threshold[t])
			Fx_regression.append(F_threshold[previous_t])
			R_regression.append(R[t])

	x = [Fx_regression, R_regression]
	return [Fy_regression, x]

def F_prevision(time, alpha, beta, gamma, F_threshold):

	t0 = max(F_threshold)
	F0 = F_threshold[t0]

	tFinal = int(timestampRoundToThreshold(time))

	times = range (t0, tFinal, thresholdInMinutes)
	#print len(times)

	R = weatherRound.getNearestPrecipitationsForPrevision(times, weatherValidityHours, db_path)
	#print R

	F1 = 0.0 
	t1 = t0 + thresholdInMinutes

	while t1 < (time - thresholdInMinutes):
		if R[t1] is None:
			F1 = alpha * F0 + gamma #assume precipitation = 0 if unknown
		else:
			F1 = alpha * F0 + beta * R[t1] + gamma


		t0 = t1
		t1 = t1 + thresholdInMinutes
		F0 = F1

	return round(F1,2)





def previsions(t, stationId, dayTemperatureAvg, dayPrecipitationTotal, isVacation):

	db = sqlite3.connect(db_path)
	cursor = db.cursor()


	L_reg_start = timeit.default_timer()
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
	A_mod_d7_stands = dailyCyclicMeans(cyclicL_stands,thresholdInMinutes)

	A_d_d_bikes = dayMeans('bike', stationId, cursor)
	A_d_d_stands = dayMeans('stand', stationId, cursor)

	[L_mod_t_bikes, F_bikes] = L_mod_t_and_F(stationId, cyclicL_bikes, A_mod_d7_bikes, A_d_d_bikes)
	[L_mod_t_stands, F_stands] = L_mod_t_and_F(stationId, cyclicL_stands, A_mod_d7_stands, A_d_d_stands)

	#regression for constant a0
	[c1_bikes, A0_bikes, AmodDifferenceD7_bikes] = a0Regression(A_mod_d7_bikes, A_d_d_bikes)
	[c1_stands, A0_stands, AmodDifferenceD7_stands] = a0Regression(A_mod_d7_stands, A_d_d_stands)

	#substract a0 from A_d for next regression
	A_d_d_bikes_minus_a0 = substract_a0_from_Ad(c1_bikes, A0_bikes, AmodDifferenceD7_bikes, A_d_d_bikes)
	A_d_d_stands_minus_a0 = substract_a0_from_Ad(c1_stands, A0_stands, AmodDifferenceD7_stands, A_d_d_stands)

	#get daily weather data
	[tempMean, tempStdDev, precStdDev, normalizedTemperatures, normalizedPrecipitations] = getDailyWeatherData()
	#get vacation data
	vacation = getVacationData()

	#daily regression
	[y_dailyRegression_bikes, x_dailyRegression_bikes] = prepareDataForDailyRegression(A_d_d_bikes_minus_a0, normalizedTemperatures, normalizedPrecipitations, vacation)
	[C1_bikes, C2_bikes, C3_bikes , K_bikes] = multilinearRegression.simpleMultipleRegression(y_dailyRegression_bikes, x_dailyRegression_bikes)

	[y_dailyRegression_stands, x_dailyRegression_stands] = prepareDataForDailyRegression(A_d_d_stands_minus_a0, normalizedTemperatures, normalizedPrecipitations, vacation)
	[C1_stands, C2_stands, C3_stands , K_stands] = multilinearRegression.simpleMultipleRegression(y_dailyRegression_stands, x_dailyRegression_stands)
	L_reg_end = timeit.default_timer()

	#L_mod prevision
	T = (dayTemperatureAvg - tempMean) / tempStdDev
	Precip = dayPrecipitationTotal / precStdDev

	L_prev_start = timeit.default_timer()
	L_prev_bikes = L_mod_prevision(t, cyclicL_bikes, A_mod_d7_bikes, A0_bikes, c1_bikes, AmodDifferenceD7_bikes,C1_bikes, C2_bikes, C3_bikes, K_bikes, T, Precip, isVacation)
	L_prev_stands = L_mod_prevision(t, cyclicL_stands, A_mod_d7_stands, A0_stands, c1_stands, AmodDifferenceD7_stands, C1_stands, C2_stands, C3_stands, K_stands, T, Precip, isVacation)
	L_prev_end = timeit.default_timer() 

	F_reg_start = timeit.default_timer()
	F_threshold_bikes = fluctuationThresholdMeans(F_bikes)
	F_threshold_stands = fluctuationThresholdMeans(F_stands)

	#fluctuation regression : F(t) = alpha * F(t-1) + beta * R(t) + gamma
	[y_fluctuationRegression_bikes, x_fluctuationRegression_bikes] = prepareDataForFluctuationRegression(F_threshold_bikes, weatherValidityHours)
	[alpha_bikes, beta_bikes, gamma_bikes] = multilinearRegression.simpleMultipleRegression(y_fluctuationRegression_bikes, x_fluctuationRegression_bikes)

	[y_fluctuationRegression_stands, x_fluctuationRegression_stands] = prepareDataForFluctuationRegression(F_threshold_stands, weatherValidityHours)
	[alpha_stands, beta_stands, gamma_stands] = multilinearRegression.simpleMultipleRegression(y_fluctuationRegression_stands, x_fluctuationRegression_stands)
	F_reg_end = timeit.default_timer()

	F_prev_start = timeit.default_timer()
	F_prev_bikes = F_prevision(t, alpha_bikes, beta_bikes, gamma_bikes, F_threshold_bikes)
	F_prev_stands = F_prevision(t, alpha_stands, beta_stands, gamma_stands, F_threshold_stands)
	F_prev_end = timeit.default_timer() 

	print 'time to compute regression for prevision without fluctuations' , (L_reg_end - L_reg_start) , 'sec'
	print 'time to compute regression for prevision with fluctuations' , ((F_reg_end - F_reg_start) + (L_reg_end - L_reg_start)) , 'sec'
	print 'time to compute prevision without fluctuations' , (L_prev_end - L_prev_start) , 'sec'
	print 'time to compute prevision with fluctuations' , ((F_prev_end - F_prev_start) + (L_prev_end - L_prev_start)) , 'sec'


	prev_bikes = L_prev_bikes + F_prev_bikes
	prev_stands = L_prev_stands + F_prev_stands

	db.close()
	
	return [prev_bikes, prev_stands, L_prev_bikes, L_prev_stands]

def displayPrevisions(previsions, stationId, t):

	[prev_bikes, prev_stands, prev_bikes_without_fluctuations, prev_stands_without_fluctuations] = previsions
	db = sqlite3.connect(db_path)
	cursor = db.cursor()
	sName = stationName(stationId)

	print ''
	print 'previsions for station', sName, '(', (stationId), ')', 'at', datetime.datetime.fromtimestamp(t)
	print 'available bikes without fluctuations:', prev_bikes_without_fluctuations
	print 'available bikes with fluctuations:', prev_bikes
	print 'available stands without fluctuations:', prev_stands_without_fluctuations
	print 'available stands with fluctuations:', prev_stands

##########################################################################################################
db_path = '../../data/velos_bdd'
db = sqlite3.connect(db_path)
cursor = db.cursor()

# prevision algorithm parameters
thresholdInMinutes = 30 # prevision precision threshlod in minutes (between 1 and 60)
weatherValidityHours = 4 # maximum validity of hourly weather data (in hours)

# station
stationId = 10113

# date/time of prevision
t_test = util.datetimeToTimestamp(datetime.datetime(2015,05,03,17))

# weather and vacation data for time of prevision (hardcoded now but should be retrieved automatically from DB later)
dailyMeanT = 20 # daily mean temperature for the day of the prevision (Celsius)
dailyTotalPrecip = 0 #sum of precipitations for the day of the prevision (mm)
vacation = 1 # set 1 is day of prevision is holiday, else 0 

displayPrevisions(previsions(t_test, stationId, dailyMeanT, dailyTotalPrecip, vacation), stationId, t_test)

db.close()

