#!/usr/bin/env python
# encoding: utf-8

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
    from DjangoBlog.utils import common_markdown
    return mark_safe(common_markdown.get_markdown(content))


@register.filter(is_safe=True)
@stringfilter
def truncatechars_content(content):
    """
    获得文章内容的摘要
    """
    from django.template.defaultfilters import truncatechars_html

    return truncatechars_html(content, settings.ARTICLE_SUB_LENGTH)

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

    return {
            'recent_articles':recent_articles,
            'sidebar_categorys':sidebar_categorys,
            'most_read_articles':most_read_articles,
            'article_dates':dates,
            'sidabar_links':links,
            'sidebar_comments':comment_list,
            'user':user,
            'show_adsense':show_adsense
            }
@register.inclusion_tag('blog/tags/article_meta_info.html')
def load_articlemetas(article,user):
    print("loadarticlemetas() enter")
    return {'article':article,
            'user':user}


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

    
