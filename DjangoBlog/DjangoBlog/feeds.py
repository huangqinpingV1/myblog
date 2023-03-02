#!/usr/bin/env python
#encoding:utf-8
from django.contrib.syndication.views import Feed
from blog.models import Article
from django.conf import settings

class DjangoBlogFeed(Feed):
    title = "%s %s "  %(settings.SITE_NAME,settings.SITE_DESCRIPTION)
    link ='/feed'

    def items(self):
        return Article.objects.order_by('-pub_time')[:5]

    def item_title(self,item):
        return item.title

    def item_description(self,item):
        return body
    
    def item_link(self,item):
        return item.get_absolute_url()
