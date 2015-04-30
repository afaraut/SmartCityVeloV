from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'getYourBike.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^$', 'search.views.search', name='search'),
	url(r'^map', 'search.views.map', name='map'),
	url(r'^stations', 'search.views.stations', name='stations'),
]
