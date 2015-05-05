from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'getYourBike.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^search$', 'search.views.search', name='search'),
	url(r'^test$', 'search.views.test', name='test'),
	url(r'^prevision/(?P<idstation>[0-9]+)/(?P<timestamp>[0-9]+)$', 'prevision'),
	url(r'^search_m$', 'search.views.search_mobile', name='search_m'),
	url(r'^map', 'search.views.map', name='map'),
	url(r'^stations', 'search.views.stations', name='stations'),
]
