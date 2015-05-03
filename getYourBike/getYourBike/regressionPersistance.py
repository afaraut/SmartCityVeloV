import pickle
import os.path
import sqlite3


base_path = '../../data/regression'
allRegressionObjects = ['cyclicL_bikes', 'cyclicL_stands', 'A_mod_d7_bikes', 'A_mod_d7_stands', 'a0Regression_bikes', 'a0Regression_stands', 'dailyRegressionCoefs_bikes', 'dailyRegressionCoefs_stands', 'F_threshold_bikes', 'F_threshold_stands', 'fluctuationRegressionCoefs_bikes', 'fluctuationRegressionCoefs_stands']
commonObjects = ['dailyWeatherData', 'vacationData']

def getFilepath(stationId, filename):
	return base_path + '/' + str(stationId) + '/' + filename

def getCommonFilepath(filename):
	return base_path + '/common/' + filename

def save(object, stationId, objectName):
	filepath = getFilepath(stationId, objectName)
	with open(filepath,'wb') as f:
		pickle.dump(object,f)

def saveCommon(object, objectName):
	filepath = getCommonFilepath(objectName)
	with open("/home/getyourbike/projects/SmartCityVeloV/data/regression/common/dailyWeatherData",'wb') as f:
		pickle.dump(object,f)

def load(stationId, objectName):
	filepath = getFilepath(stationId, objectName)
	with open(filepath,'rb') as f:
		object = pickle.load(f)
	return object

def loadCommon(objectName):
	filepath = getCommonFilepath(objectName)
	with open(filepath,'rb') as f:
		object = pickle.load(f)
	return object

def checkObjectsExistence(stationId):
	for objectName in allRegressionObjects:
		filepath = getFilepath(stationId, objectName)
		if not os.path.exists(filepath):
			return False
	return True

def checkCommonObjectsExistence():
	for objectName in commonObjects:
		filepath = getCommonFilepath(objectName)
		if not os.path.exists(filepath):
			return False
	return True

def ensureDirectory(stationId):
	directory = base_path + '/' + str(stationId)
	if not os.path.exists(directory):
		os.makedirs(directory)

def createAllDirectories(db_path):
	db = sqlite3.connect(db_path)
	cursor = db.cursor()
	for data in cursor.execute('SELECT DISTINCT stationId FROM OldResults '):
		ensureDirectory(str(data[0]))
	ensureDirectory('common')

