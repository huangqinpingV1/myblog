#!/usr/bin/env python
#encoding:utf-8
from haystack import indexes
from django.conf import settings
from .models import Article,Category,Tag

#类名必须为需要检索的model+Index命名,这里需要检索检索Article,所以创建的类是ArticleIndex类
class ArticleIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document  = True,use_template = True)
    
    #重载指定查询的model
    def get_model(self):
        return Article
    #重载
    def index_queryset(self,using=None):
        print("index_queryset() enter")
        return self.get_model().objects.filter(status ='p')

"""
class CategoryIndex(indexes.SearchIndex,indexes.Indexable):
    name = indexes.CharField(document=True,use_template= True)

    def get_model(self):
        return Article

    def index_queryset(self,using=None):
        return self.get_model().objects.filter(status='p')
"""        
