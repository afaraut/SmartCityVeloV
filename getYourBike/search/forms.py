#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
from search.models import Station

class SearchForm(forms.Form):
    day = forms.DateField(widget=extras.SelectDateWidget, label="Jour")
    hour = forms.TimeField(widget=SelectTimeWidget, label="Heure ")
    station = forms.CharField(widget=forms.Select, label=u'Station')

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        stations = Station.objects.all()
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(stationn.stationNum,  (stationn.stationRegion).encode('utf8') + str(" -- " ) + (stationn.stationName).encode('utf8')) for stationn in stations]), label="Station")

