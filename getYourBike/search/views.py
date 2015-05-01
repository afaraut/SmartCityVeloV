#!/usr/bin/python
#-*- coding: utf-8 -*-

from search.forms import SearchForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
import csv
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@api_view(['GET'])
def search(request):
    """
        BLAH BLAH
    """
    content = {"manual" : "bonjour"}  
    return Response(content, template_name='search/search.html')

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
            result = "OK"
            day_month = request.POST.get('day_month')
            day_day = request.POST.get('day_day')
            day_year = request.POST.get('day_year')
            hour_hour = request.POST.get('hour_hour')
            hour_minute = request.POST.get('hour_minute')
            station = request.POST.get('station')
        else:
            result = "NOK"

    return Response(locals(), template_name='home.html') # Return the response

#test
@csrf_exempt
def stations(request):
    cr = csv.reader(open('/home/getyourbike/projects/SmartCityVeloV/longLat.csv',"rb"))
    data = []
    for raw in cr:
        dict = {}
        dict['num'] = raw[0]
        dict['nom'] = raw[1]
        dict['arr'] = raw[2]
        dict['lat'] = raw[3]
        dict['lon'] = raw[4]
        dict['available'] = raw[6]
        data.append(dict)
    # on fait un retour au client
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")