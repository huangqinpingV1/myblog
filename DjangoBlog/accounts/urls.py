#!/usr/bin/env python
#encoding:utf-8
from django.urls import path
from .forms import LoginForm
from django.contrib.auth import views as auth_view
from . import views
app_name ='accounts'
urlpatterns =[
        path('login/',views.LoginView.as_view(success_url='/'),name='login',kwargs={'authentication_form':LoginForm}),
        path('register/',views.RegisterView.as_view(success_url='/'),name='register'),
        path('logout/',views.logout,name='logout')
        ]
