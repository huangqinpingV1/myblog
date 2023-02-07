from django.urls import path
from . import views
urlpatterns  =[
    path(r'',views.IndexView.as_view(),name='index'),    
    ]
