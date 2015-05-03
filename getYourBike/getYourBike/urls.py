from django.conf.urls import patterns, include, url
from django.contrib import admin

#urlpatterns = [
    # Examples:
    # url(r'^$', 'getYourBike.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^search/', include('search.urls')),
#]


urlpatterns = patterns('',
    url(r'^$', 'search.views.home'),
    url(r'^search/', include('search.urls')),
    url(r'^admin/', include(admin.site.urls)),

)