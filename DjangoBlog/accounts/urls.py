#!/usr/bin/env python
#encoding:utf-8
from django.urls import path
from .froms import LoginForm

urlpatterns =[
        path('login/',views.LoginView.as_view(success_url='/'),name='login',kwargs={'authenication_form':LoginForm}),
        path('register/',views.RegisterView.as_view(success_url='/'),name='register'),
        ]
