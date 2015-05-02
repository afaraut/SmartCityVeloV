import prevision
import util
import datetime


# station
stationId = 1001

# date/time of prevision ()
t_prevision = util.datetimeToTimestamp(datetime.datetime(2015,05,10,15)) #GMT time

prev = prevision.previsions(t_prevision, stationId)
prevision.displayPrevisions(prev, stationId, t_prevision)
