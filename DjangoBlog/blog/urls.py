from django.urls import path
from . import views
#如果引用blog的url使用的include中指定了namespace则必须定义app_name或者在include中指定app_name
app_name  = "blog"
urlpatterns  =[
    path(r'',views.IndexView.as_view(),name='index'),    
    ]
