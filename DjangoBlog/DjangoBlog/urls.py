"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#增加站点地图
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSitemap,ArticleSiteMap,CategorySiteMap,TagSiteMap,UserSiteMap
from .feeds import DjangoBlogFeed
sitemaps ={
        'blog':ArticleSiteMap,
        'Category':CategorySiteMap,
        'Tag':TagSiteMap,
        'User':UserSiteMap,
        'static':StaticViewSitemap,
        }


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls',namespace ='blog')),
    #增加评论url
    path('',include('comments.urls',namespace='comments')),
    #账号相关url
    path('',include('accounts.urls',namespace='accounts')),
    path('',include('oauth.urls',namespace='oauth')),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('feed',DjangoBlogFeed()),
    #添加搜索相关功能
    path('search',include('haystack.urls'),name='search'),
    ]
