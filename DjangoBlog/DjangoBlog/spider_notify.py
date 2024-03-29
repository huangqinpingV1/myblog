#!/usr/bin/env python
#encoding:utf-8
from django.contrib.sitemaps import ping_google
import requests
from django.conf import settings

class SpiderNotify():
    @staticmethod
    def baidu_notify(self,urls):
        try:
            data  = '\n'.join(urls)
            result = requests.post(settings.BAIDU_NOTIFY_URL,data=url)
            print(result.text)
        except Exception as e:
            print(e)
    @staticmethod 
    def __google_notify(self):
        try:
            ping_google('/sitemap.xml')
        except Exception as e:
            print(e)
    @staticmethod 
    def notify(self,url):
         SpiderNotify.baidu_notify(url)
         SpiderNotify.__google_notify()
