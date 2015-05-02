#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
from search.models import Station

class SearchForm(forms.Form):
    day = forms.DateField(widget=extras.SelectDateWidget, label="Veuillez choisir votre jour ")
    hour = forms.TimeField(widget=SelectTimeWidget, label="Veuillez choisir votre heure ")
    station = forms.CharField(widget=forms.Select, label=u'Veuillez choisir votre station ')

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        stations = Station.objects.all()
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(Station.stationNum, str(station.stationRegion + " -- " + station.stationName)) for station in stations]), label="Veuillez choisir votre station ")