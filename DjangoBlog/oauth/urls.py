#!/usr/bin/env python
#encoding:utf-8

from django.urls import  path
from . import views
app_name= 'oauth'
urlpatterns=[
        path('oauth/wbauthorize/',views.authorize),
        ]

