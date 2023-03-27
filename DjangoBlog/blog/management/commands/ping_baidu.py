#!/usr/bin/env pyhon
#encoding:utf-8
from  django.core.management.base import BaseCommand,CommandError
from blog.models import Article
from DjangoBlog.spider_notify import sipder_notify

class Command(BaseCommand):
    help = 'notify baidu url'

    def handle(self,*args,**options):
        notify = sipder_notify()
        for article in Article.objects.filter(status='p'):
            try:
                url= article.get_full_url()
                notify.baidu_notify(url=url)
                self.stdout.write(self.style.SUCCESS('Successfully notify article id:"%s"' % article.pk))
            except Exception as e:
                self.stdout.write('error:'+str(e))
           
           self.stdout.write(self.style.SUCCESS('finish notify'))
