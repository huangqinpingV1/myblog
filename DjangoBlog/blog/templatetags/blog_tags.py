#!/usr/bin/env python
#encoding: utf-8

from django import template
from django.conf import settings
import markdown2
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import random
from blog.models  import Article,Category,Tag,Links
from django.utils.encoding import force_str
import hashlib
import urllib
from comments.models import Comment
from DjangoBlog.utils import logger
from django.urls import reverse
import traceback
#注册自定义标签
register = template.Library()

#添加自定义标签
@register.simple_tag
def timeformat(data):
    print("timeformat() enter")
    try:
        return data.strftime(settings.TIME_FORMAT)
    except:
        return ""

@register.simple_tag
def datetimeformat(data):
    print("datetimeformat() enter")
    try:
        return data.strftime(settings.DATE_TIME_FORMAT)
    except:
        return ""

@register.filter(is_safe = True)
@stringfilter
def custom_markdown(content):
    print("custom_markdown() enter")
    from DjangoBlog.utils import CommonMarkdown
    return mark_safe(CommonMarkdown.get_markdown(content))


@register.filter(is_safe=True)
@stringfilter
def truncatechars_content(content):
    """
    获得文章内容的摘要
    """
    from django.template.defaultfilters import truncatechars_html

    return truncatechars_html(content, settings.ARTICLE_SUB_LENGTH)
@register.filter(is_safe =True)
@stringfilter
def truncate(content):
    from django.utils.html import strip_tags
    return strip_tags(content)[:150]

@register.inclusion_tag('blog/tags/breadcrumb.html')
def load_breadcrumb(article):
    names  = article.get_category_tree()
    names.append((settings.SITE_NAME,settings.SITE_URL))
    names = names[::-1]
    print("parsecategoryname() enter")
    return {
            'names':names,
            'title': article.title
            }


@register.inclusion_tag('blog/tag/article_tag_list.html')
def load_articletags(article):
    print("loadarticletags() enter")
    tags = article.tags.all()
    tags_list =[]
    for tag in tags:
        url = tag.get_absolute_url()
        count = tag.get_article_count()
        tags_list.append((url,count,tag,random.choice(settings.BOOTSTRAP_COLOR_TYPES)))

    return {'article_tags_list' : tags_list}

@register.inclusion_tag('blog/tags/sidebar.html')
def load_sidebar(user):
    print("loadsidebartags() enter")
    recent_articles = Article.objects.filter(status='p')[::settings.SIDEBAR_ARTICLE_COUNT]
    sidebar_categorys = Category.objects.all()
    most_read_articles = Article.objects.filter(status = 'p').order_by('-views')[::settings.SIDEBAR_ARTICLE_COUNT]
    dates = Article.objects.datetimes('created_time','month',order ='DESC')
    links = Links.objects.all()
    comment_list = Comment.objects.order_by('-id')[:settings.SIDEBAR_COMMENT_COUNT]
    show_adsense  = settings.SHOW_GOOGLE_ADSENSE
    #tags
    #根据云 计算字体大小
    #根据总数计算出平均值，大小为(数目/平均值)
    increment = 10
    tags  = Tag.objects.all()
    sidebar_tags = None
    if tags:
        s = list(map(lambda t:(t,t.get_article_count()),tags))
        count = sum(map(lambda t:t[1],s))
        dd = count /len(tags)
        sidebar_tags = list(map(lambda x:(x[0],x[1],(x[1]/dd)*increment),s))
    return {
            'recent_articles':recent_articles,
            'sidebar_categorys':sidebar_categorys,
            'most_read_articles':most_read_articles,
            'article_dates':dates,
            'sidabar_links':links,
            'sidebar_comments':comment_list,
            'user':user,
            'show_adsense':show_adsense,
            'sidebar_tags':sidebar_tags
            }
@register.inclusion_tag('blog/tags/article_meta_info.html')
def load_article_metas(article,user):
    print("loadarticlemetas() enter")
    return {'article':article,
            'user':user}

@register.inclusion_tag('blog/tags/article_paginations.html')
def load_pagination_info(page_obj,page_type,tag_name):
    print("加载文章分类")
    previous_url = ''
    next_url = ''

    if page_type  == '':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:index_page',kwargs={'page':next_number})

        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:index_page',kwargs={'page':previous_number})
        
    if page_type == '分类标签归档':
            if page_obj.has_next():
                next_number = page_obj.next_page_number()
                next_url = reverse('blog:tag_detail_page',kwargs={'page':next_number,'tag_name':tag_name})
            if page_obj.has_previous():
                previous_number = page_obj.previous_page_number()
                previous_url = reverse('blog:tag_detail_page',kwargs={'page':previous_number,'tag_name':tag_name})
    if page_type == '作者文章归档':
            if page_obj.has_next():
                next_number = page_obj.next_page_number()
                next_url = reverse('blog:author_detail_page',kwargs={'page':next_number,'author_name':tag_name})
            if page_obj.has_previous():
                previous_number = page_obj.previous_page_number()
                previous_url = reverse('blog:author_detail_page',kwargs={'page':previous_number,'author_name':tag_name})
    if page_type == '分类目录归档':
            if page_obj.has_next():
                next_number = page_obj.next_page_number()
                next_url = reverse('blog:category_detail_page',kwargs={'page':next_number,'category_name':tag_name})
            if page_obj.has_previous():
                previous_number = page_obj.previous_page_number()
                previous_url = reverse('blog:category_detail_page',kwargs={'page':previous_number,'category_name':tag_name})
    
    return {'previous_url':previous_url,
            'next_url':next_url,'page_obj':page_obj}

@register.inclusion_tag('blog/tags/article_info.html')
def load_article_detail(article,isindex,user):
    print("load_article_detail() enter")
    return {'article':article,'isindex':isindex,'user':user}


"""
@register.tag
def parseCategoryName(parser,token):
    tag_name , category = token.split_contents()
    print(category)
    print(tag_name)
    return CategoryNametag(category)

class CategoryNametag(template.Node):
    def __init__(self,category):
        self.category=category
        self.names=[]


    def parseCategory(self,category):
        self.names.append(category.name)
        if category.parent_category:
            self.parseCategory(category.parent_category)


    def render(self, context):
        self.parseCategory(self.category)
        print(self.names)
        return " > ".join(self.names)

        #if self.category.parent_category:  
"""

@register.filter
def gravatar_url(email,size =40):
    print("gravtar_url() enter")
    email= email.encode('utf-8')
    default = "xxxxxxxxxxx".encode('utf-8')

    return "xxxxxxx/%s?%s" %(hashlib.md5(email.lower()).hexdigest(),urllib.parse.urlencode({'d':default,'s':str(size)}))

@register.filter
def gravatar(email,size= 40):
    url = gravatar_url(email,size)
    return make_safe('<img src =%s> height  ="%d" width= %d>' % (url,size,size))

@register.simple_tag
def query(qs,**kwargs):
    return qs.filter(**kwargs)

    
