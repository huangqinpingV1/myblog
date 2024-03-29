#!/usr/bin/env python
#encoding:utf-8

from django.conf import settings
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend():
    """
    允许用户使用用户名和邮箱登录
    """
    def authenticate(self,username=None,password=None):
        print("用户名或邮箱登录:"+username)
        if '@' in username:
            kwargs = {'email':username}
        else :
            kwargs  ={'username':username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None


    def get_user(self,username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
