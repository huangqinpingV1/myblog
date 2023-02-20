#!/usr/bin/env python
#encoding: utf-8
from django.urls import path
from . import views
app_name =  'comments'
urlpatterns = [
        path('article/<article_id>/postcomment',views.CommentPostView.as_view(),name='postcomment'),
        ]
