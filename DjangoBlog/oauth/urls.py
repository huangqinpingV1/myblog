#!/usr/bin/env python
#encoding:utf-8

from django.urls import  path
from . import views
app_name= 'oauth'
urlpatterns=[
        path('oauth/wbauthorize/',views.authorize),
        path('oauth/requireemail/<oauthid>.html',views.RequireEmailView.as_view(),name='require_email'),
        path('oauth/emailconfirm/<id>/<sign>.html',views.emailconfirm,name='email_confirm'),
        path('oauth/bindsuccess/<oauthid>.html',views.bindsuccess,name='bindsuccess'),
        ]

