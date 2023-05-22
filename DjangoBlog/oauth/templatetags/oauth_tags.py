#!/usr/bin/env python 
#encoding:utf-8

from oauth.oauthmanager import *
from django import template
from django.conf import settings
from oauth.oauthmanager import   get_oauth_apps
register = template.Library()

@register.inclusion_tag('oauth/oauth_applications.html')
def load_oauth_applications():
    applications  = get_oauth_apps()
    apps  = list(map(lambda x:(x.ICON_NAME,x.get_authorization_url() ),applications))
    return  {'apps': apps}    
