#!/usr/bin/env python
#encoding:utf-8
from django.urls import path
from .forms import LoginForm
from . import views
app_name ='accounts'
urlpatterns =[
        path('login/',views.LoginView.as_view(success_url='/'),name='login',kwargs={'authenication_form':LoginForm}),
        path('register/',views.RegisterView.as_view(success_url='/'),name='register'),
        ]
