#!/usr/bin/env python 
#encoding:utf-8

from oauth.oauthmanager import *
from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('oauth/oauth_applications.html')
def load_oauth_applications():
    applications = BaseOauthManager.__subclasses__()
    apps  = []

    for application in applications:
        app = application()
        icon = app.ICON_NAME
        authorizeurl = app.get_authorization_url()
        apps.append((icon,authorizeurl))

    return  {'apps': apps}    
