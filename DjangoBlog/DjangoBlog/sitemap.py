#!/usr/bin/env python
#encoding:utf-8
from django.contrib.sitemaps import Sitemap
from blog.models import Article,Category,Tag
from accounts.models import BlogUser
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['blog:index',]

    def location(self,item):
        return reverse(item)


class ArticleSiteMap(Sitemap):
    priority ='0.6'
    changefreq = 'monthly'

    def items(self):
        return Article.objects.filter(status='p')

    def lastmod(self,obj):
        return obj.last_mod_time


class CategorySiteMap(Sitemap):
    priority = '0.6'
    changefreq = 'Weekly'

    def items(self):
        return Category.objects.all()

    def lastmod(self,obj):
        return obj.last_mod_time

class TagSiteMap(Sitemap):
    changefreq ='Weekly'
    priority = '0.3'


    def items(self):
        return Tag.objects.all()

    def lastmod(self,obj):
        return obj.last_mod_time

class UserSiteMap(Sitemap):
    changefreq ='Weekly'
    priority = '0.3'

    def items(self):
        return BlogUser.objects.all()

    def lastmod(self,obj):
        return obj.date_joined

