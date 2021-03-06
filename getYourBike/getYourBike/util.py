#!/usr/local/bin/python
# -*- coding: utf-8	 -*-

import time
import datetime

def is_number(s):
	try:
		if s == None:
			return False
		float(s)
		return True
	except ValueError:
		return False

def datetimeToTimestamp(dt):
	return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

def timestampToDayOfWeek(timestamp):
	#in strftime sunday = 0, saturday = 6 -> convert to monday = 0, sunday = 6
	dateFromTimestamp = datetime.datetime.fromtimestamp(timestamp)
	return (int(datetime.datetime.strftime(dateFromTimestamp,"%w"))+6) % 7 

def timestampToDatetime(timestamp):
	return datetime.datetime.fromtimestamp(timestamp)