import datetime
import time


import prevision
import previsionEvaluation
import util

# station
stationId = 1001

# date/time of prevision ()
t_prevision = util.datetimeToTimestamp(datetime.datetime(2015,05,10,15)) #GMT time
t_request = int(time.time())

prev = prevision.previsions(t_prevision, stationId)
prevision.displayPrevisions(prev, stationId, t_prevision)

#save prevision in DB for future evaluation
previsionEvaluation.savePrevision(prev, stationId, t_request, t_prevision)