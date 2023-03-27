#!/usr/bin/env python
#encoding:utf-8
from django.contrib.sitemaps import ping_google
import requests
from django.conf import settings

class sipder_notify():
    def baidu_notify(self,url):
        try:
            result = requests.post(settings.BAIDU_NOTIFY_URL,data=url)
            print(result.text)
        except Exception as e:
            print(e)
     
    def __google_notify(self):
        try:
            ping_google('/sitemap.xml')
        except Exception as e:
            print(e)
     
    def notify(self,url):
         self.baidu_notify(url)
         self.__google_notify()
