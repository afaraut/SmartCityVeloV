#!/usr/bin/python
#-*- coding: utf-8 -*-
from search.forms import SearchForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import RequestContext, loader
import json, csv, codecs, time, datetime
from django.views.decorators.csrf import csrf_exempt
from search.models import Station
from getYourBike.prevision import previsions
# Create your views here.

def date2Timestamp(hour, formatage="%Y/%m/%d %H:%M"):
    """This function allows to convert a date into a timestamp"""
    return int(time.mktime(datetime.datetime.strptime(hour, formatage).timetuple()))
@csrf_exempt
def search(request):
	day_month = request.POST.get('day_month')
	day_day = request.POST.get('day_day')
	day_year = request.POST.get('day_year')
	hour_hour = request.POST.get('hour_hour')
	hour_minute = request.POST.get('hour_minute')
	station = request.POST.get('station')
	hour = "%s/%s/%s %s:%s" % (day_year, day_month, day_day, hour_hour, hour_minute)
	timestamp = date2Timestamp(hour)
	prev = previsions(timestamp, station)
	result = prev
	content = json.dumps(result)
	return HttpResponse(content, content_type="application/json")
	
def search_mobile(request):
	day_month = request.GET.get('day_month')
	day_day = request.GET.get('day_day')
	day_year = request.GET.get('day_year')
	hour_hour = request.GET.get('hour_hour')
	hour_minute = request.GET.get('hour_minute')
	station = request.GET.get('station')
	hour = "%s/%s/%s %s:%s" % (day_year, day_month, day_day, hour_hour, hour_minute)
	timestamp = date2Timestamp(hour)
	prev = previsions(timestamp, station)
	result = prev
	content = json.dumps(result)
	return HttpResponse(content, content_type="application/json")
def map(request):
    template = loader.get_template('search/map.html')
    return HttpResponse(template.render())



@api_view(['GET', 'POST'])
def home(request):
    """
        This function is called for display the Home page
        @param request : Contains the query parameters
        This function just accepts the GET method
    """
    if request.method == 'GET': # For the GET method
        form = SearchForm()  # Nous creons un formulaire vide
    elif request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formulaire = SearchForm(request.POST)
        # check whether it's valid:
        if formulaire.is_valid():
            day_month = request.POST.get('day_month')
            day_day = request.POST.get('day_day')
            day_year = request.POST.get('day_year')
            hour_hour = request.POST.get('hour_hour')
            hour_minute = request.POST.get('hour_minute')
            station = request.POST.get('station')
            hour = "%s/%s/%s %s:%s" % (day_year, day_month, day_day, hour_hour, hour_minute)
            timestamp = date2Timestamp(hour)
            prev = previsions(timestamp, station)
            result = prev
        else:
            result = "NOK"

    return Response(locals(), template_name='home.html') # Return the response

#test
@csrf_exempt
def stations(request):
    #cr = csv.reader(open('static/longLat.csv',"rb", ))
    stations = Station.objects.all()
    #fichier = codecs.open("stations", 'w', encoding='utf-8')
    #fichier.write('[')
    data = []
    #cpt = 1
    for station in stations:
        dict = {}
        dict['stationNum'] = station.stationNum
        dict['stationName'] = station.stationName
        dict['stationRegion'] = station.stationRegion
        dict['stationLong'] = station.stationLong
        dict['stationLat'] = station.stationLat
        #if cpt != 1:
            #fichier.write(',')
        #fichier.write('{ "model" : "search.station", "pk" : ' + str(cpt) + ', "fields" : ' + str(json.dumps(dict)) + "}")
        #cpt = cpt + 1
        #dict['available'] = raw[6]
        data.append(dict)
    #fichier.write(']')
    #fichier.close()
    # on fait un retour au client
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")