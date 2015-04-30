from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
import csv
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@api_view(['GET'])
def home(request):
    """
        This function is called for display the Home page
        @param request : Contains the query parameters
        This function just accepts the GET method
    """
    return Response(template_name='home.html') # Return the response

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
	cr = csv.reader(open('/home/getyourbike/projects/SmartCityVeloV/longLat.csv',"rb"))
	data = []
	for raw in cr:
		dict = {}
		dict['num'] = raw[0]
		dict['nom'] = raw[1]
		dict['arr'] = raw[2]
		dict['lat'] = raw[3]
		dict['lon'] = raw[4]
		
		data.append(dict)
	
	# on fait un retour au client
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")
