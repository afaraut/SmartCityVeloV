#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
from search.models import Station
import datetime, time

class SearchForm(forms.Form):
    day = forms.DateField(widget=extras.SelectDateWidget, initial=datetime.date.today(), label="Jour")
    hour = forms.DateTimeField(widget=SelectTimeWidget(minute_step=5), initial=datetime.datetime.utcnow(), label="Heure ")
    station = forms.CharField(widget=forms.Select, label=u'Station')

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        stations = Station.objects.all()
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(stationn.stationNum,  (stationn.stationRegion).encode('utf8') + str(" -- " ) + (stationn.stationName).encode('utf8')) for stationn in stations]), label="Station")

