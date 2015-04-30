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
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        	result = "OK"
        result = "NOK"

    return Response(locals(), template_name='home.html') # Return the response

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

#test
@csrf_exempt
def stations(request):
	Fichier = open('test.log', 'w')
	cr = csv.reader(open('C:\longLat.csv',"rb"))
	data = []
	
	
	for raw in cr:
		dict = {}
		dict['lon'] = raw[4]
		dict['lat'] = raw[3]
		data.append(dict);
		
		
	#post = request.POST['list_bouteille']
	#list_bouteille = json.loads(post)
	#Fichier.write(len(list_bouteille))
	
	Fichier.write("ok");
	# on fait un retour au client
	json_data = json.dumps(data)
	Fichier.close()
	return HttpResponse(json_data, content_type="application/json")