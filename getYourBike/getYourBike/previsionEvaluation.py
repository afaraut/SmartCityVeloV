#!/usr/local/bin/python
# -*- coding: utf-8	 -*-

import sqlite3

from paths import db_path_string

def savePrevision(prevision, stationId, requestTimestamp, previsionTimestamp):
	[prev_bikes, prev_stands, prev_bikes_without_fluctuations, prev_stands_without_fluctuations] = prevision

	db = sqlite3.connect(db_path_string)
	cursor = db.cursor()

	cursor.execute('INSERT INTO Request(stationId, requestDate, previsionDate, realAvailableBikes, realAvailableStands, previsionAvailableBikes, \
		previsionAvailableStands, previsionAvailableBikesFluct, previsionAvailableStandsFluct) VALUES(?,?,?,?,?,?,?,?,?)', \
		(stationId, requestTimestamp, previsionTimestamp, None, None, prev_bikes_without_fluctuations, prev_stands_without_fluctuations, prev_bikes, prev_stands))

	db.close()