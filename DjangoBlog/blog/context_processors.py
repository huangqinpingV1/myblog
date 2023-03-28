#!/usr/bin/env python
# encoding: utf-8
from .models import Category,Article,Tag
from django.conf import settings

def seo_processor(requests):
    return {
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
