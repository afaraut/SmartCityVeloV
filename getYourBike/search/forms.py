#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
import csv
class SearchForm(forms.Form):
    station = forms.CharField(widget=forms.Select, label=u'Station')
    day = forms.DateField(widget=extras.SelectDateWidget, label="Jour")
    hour = forms.TimeField(widget=SelectTimeWidget, label="Heure ")
    

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        cr = csv.reader(open('static/longLat.csv',"rb"))
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(raw[1], str(raw[2] + " -- " + raw[1])) for raw in cr]), label=u'Station ')