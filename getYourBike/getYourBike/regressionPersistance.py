#!/usr/local/bin/python
# -*- coding: utf-8	 -*-

import pickle
import sqlite3
import os
from pathlib import Path

from paths import db_path
from paths import regression_path
from paths import common_path


allRegressionObjects = ['cyclicL_bikes', 'cyclicL_stands', 'A_mod_d7_bikes', 'A_mod_d7_stands', 'a0Regression_bikes', 'a0Regression_stands', 'dailyRegressionCoefs_bikes', 'dailyRegressionCoefs_stands', 'F_threshold_bikes', 'F_threshold_stands', 'fluctuationRegressionCoefs_bikes', 'fluctuationRegressionCoefs_stands']
commonObjects = ['dailyWeatherData', 'vacationData']

def getFilepath(stationId, filename):
	return regression_path  / str(stationId) / filename

def getCommonFilepath(filename):
	return common_path / filename

def save(object, stationId, objectName):
	filepath = getFilepath(stationId, objectName)
	with filepath.open('wb') as f:
		pickle.dump(object,f)

def saveCommon(object, objectName):
	filepath = getCommonFilepath(objectName)
	with filepath.open('wb') as f:
		pickle.dump(object,f)

def load(stationId, objectName):
	filepath = getFilepath(stationId, objectName)
	with filepath.open('rb') as f:
		object = pickle.load(f)
	return object

def loadCommon(objectName):
	filepath = getCommonFilepath(objectName)
	with filepath.open('rb') as f:
		object = pickle.load(f)
	return object

def checkObjectsExistence(stationId):
	for objectName in allRegressionObjects:
		filepath = getFilepath(stationId, objectName)
		if not Path.exists(filepath):
			return False
	return True

def checkCommonObjectsExistence():
	for objectName in commonObjects:
		filepath = getCommonFilepath(objectName)
		if not Path.exists(filepath):
			return False
	return True

def ensureDirectory(stationId):
	directory = regression_path / str(stationId)
	if not Path.exists(directory):
		os.makedirs(directory)

def createAllDirectories(db_path):
	db = sqlite3.connect(db_path)
	cursor = db.cursor()
	for data in cursor.execute('SELECT DISTINCT stationId FROM OldResults '):
		ensureDirectory(reression_path /  str(data[0]))
	ensureDirectory(common_path)

