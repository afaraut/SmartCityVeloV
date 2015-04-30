#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget
import csv
class SearchForm(forms.Form):
    day = forms.CharField(widget=extras.SelectDateWidget, label="Veuillez choisir votre jour ")
    hour = forms.DateField(widget=SelectTimeWidget, label="Veuillez choisir votre heure ")
    station = forms.CharField(widget=forms.Select, label=u'Veuillez choisir votre station ')

    def __init__(self, *args, **kwargs):
    	super(SearchForm, self).__init__(*args, **kwargs)
        cr = csv.reader(open('D:\longLat.csv',"rb"))
        #self.fields['station'].choices = [(raw[1], raw[2]) for raw in cr]
        self.fields['station'] = forms.CharField(widget=forms.Select(choices=[(raw[1], str(raw[2] + " -- " + raw[1])) for raw in cr]), label=u'Veuillez choisir votre station ')
        # data = []
        # for raw in cr:
        #     dict = {}
        #     dict['lon'] = raw[4]
        #     dict['lat'] = raw[3]
        #     dict['arrondissement'] = raw[2]
        #     dict['place'] = raw[1]
        #     data.append(dict);
        # json_data = json.dumps(data)