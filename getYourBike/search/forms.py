#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
from search.models import Station

class SearchForm(forms.Form):
    station = forms.CharField(widget=forms.Select, label=u'Station')
    day = forms.DateField(widget=extras.SelectDateWidget, label="Jour")
    hour = forms.TimeField(widget=SelectTimeWidget, label="Heure ")
    

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        stations = Station.objects.all()
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(station.stationNum,  (station.stationRegion).encode('utf8') + str(" -- " ) + (station.stationName).encode('utf8')) for station in stations]), label="Sation")

