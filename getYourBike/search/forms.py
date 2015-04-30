#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
import csv
class SearchForm(forms.Form):
    day = forms.DateField(widget=extras.SelectDateWidget, label="Veuillez choisir votre jour ")
    hour = forms.TimeField(widget=SelectTimeWidget, label="Veuillez choisir votre heure ")
    station = forms.CharField(widget=forms.Select, label=u'Veuillez choisir votre station ')

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        cr = csv.reader(open('D:\longLat.csv',"rb"))
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(raw[1], str(raw[2] + " -- " + raw[1])) for raw in cr]), label=u'Veuillez choisir votre station ')