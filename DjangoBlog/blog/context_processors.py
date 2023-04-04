#!/usr/bin/env python
# encoding: utf-8
from .models import Category,Article,Tag
from django.conf import settings
from django.core.cache import cache
from DjangoBlog.utils import logger

def seo_processor(requests):
    key = 'seo_processor'
    value = cache.get(key)
    if value:
        logger.info('get processor cache')
        return value
    else:
        logger.info('set processor cache')
        value= {
            'SHOW_GOOGLE_ADSENSE':settings.SHOW_GOOGLE_ADSENSE,
            'SITE_NAME':settings.SITE_NAME,
            'SITE_DESCRIPTION':settings.SITE_DESCRIPTION,
            'SITE_SEO_DESCRIPTION':settings.SITE_SEO_DESCRIPTION,
            'SITE_SEO_KEYWORDS':settings.SITE_SEO_KEYWORDS,
            'SITE_BASE_URL': 'http://'+requests.get_host()+'/',
            'ARTICLE':settings.ARTICLE_SUB_LENGTH,
            'nav_category_list':Category.objects.all(),
            'nav_pages':Article.objects.filter(type='p',status='p'),
            }
        cache.set(key,value,60*60*10)
        return value
