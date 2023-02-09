#!/usr/bin/env python
# encoding: utf-8

from django import template
from django.conf import settings
import markdown
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

#注册自定义标签
register = template.Library()

#添加自定义标签
@register.simple_tag
def timeformat(data):
    try:
        return data.strtime(settings.TIME_FORMAT)
    except:
        return ""

@register.filter(is_safe = True)
@stringfilter
def custom_markdown(content):
    return mark_safe(markdown.markdown(content,extensions  =['markdown.extensions.fenced_code','markdown.extensions.codehilite'],
        safe_mode = True,enable_attributes =False))


@register.inclusion_tag('categorytree.html')
def parseCategoryName(article):
    names  = article.getCategoryNameTree()
    names.append((settings.SITE_NAME,'http://127.0.0.1:8080'))
    names = names[::-1]
    print(names)
    return {'names':names}


