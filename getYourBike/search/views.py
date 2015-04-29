from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

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