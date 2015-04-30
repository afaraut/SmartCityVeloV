#!/usr/bin/python
#-*- coding: utf-8 -*-
from django import forms
from django.forms import extras
from search.models import SelectTimeWidget

class SearchForm(forms.Form):
    day = forms.CharField(widget=extras.SelectDateWidget, label="Veuillez choisir votre jour ")
    hour = forms.DateField(widget=SelectTimeWidget, label="Veuillez choisir votre heure ")
    station = forms.CharField(label="Veuillez choisir votre station ")
    