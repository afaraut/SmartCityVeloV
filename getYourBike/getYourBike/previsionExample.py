#!/usr/local/bin/python
# -*- coding: utf-8	 -*-

import datetime
import time

import prevision
import previsionEvaluation
import util
import paths

# station
stationId = 1001

# date/time of prevision ()
t_prevision = int(util.datetimeToTimestamp(datetime.datetime(2015,02,05,10,07,00))) #GMT time
t_request = int(time.time())

print t_prevision
print t_request
print util.timestampToDatetime(t_prevision)
print util.timestampToDatetime(t_request)


prev = prevision.previsions(t_prevision, stationId)
prevision.displayPrevisions(prev, stationId, t_prevision)

#save prevision in DB for future evaluation
previsionEvaluation.savePrevision(prev, stationId, t_request, t_prevision)