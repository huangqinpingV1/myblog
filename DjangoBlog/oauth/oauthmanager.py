#!/usr/bin/env python
#encoding:utf-8

from abc import ABCMeta,abstractmethod,abstractproperty
import requests
import json
import urllib.parse
from DjangoBlog.utils import logger,parse_dict_to_url
from django.conf import settings
from oauth.models import OAuthUser

class BaseOauthManager(metaclass=ABCMeta):
    """获取用户授权"""
    AUTH_URL = None
    """获取token"""
    TOKEN_URL = None
    """获取用户信息"""
    API_URL = None
    """icon图标名"""
    ICON_NAME = None

    def __init__(self,access_token = None,openid =None):
        self.access_token = access_token
        self.openid = openid

    @property
    def is_access_token_set(self):
        return self.access_token is not  None

    @property
    def is_authorized(self):
        return self.is_access_token_set and self.access_token is not None and self.openid is not None

    @abstractmethod
    def get_authorization_url(self):
        pass

    @abstractmethod
    def get_access_token_by_code(self,code):
        pass

    @abstractmethod
    def get_oauth_userinfo(self):
        pass

    def do_get(self,url,params):
        rsp = request.post(url,params)
        return rsp.text

class WBOauthManager(BaseOauthManager):
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    API_URL = 'https://api.weibo.com/2/users/show.json'

    def __init__(self,access_token=None,openid=None):
        self.client_id = settings.OAHUTH['sina']['appkey']
        self.client_secret = settings.OAHUTH['sina']['appsecret']
        self.callback_url =settings.OAHUTH['sina']['callbackurl']
        super(WBOauthManager,self).__init__(access_token=access_token,openid=openid)

    
    def get_authorization_url(self):
        params ={
                'client_id':self.client_id,
                'response_type':'code',
                'redirect_uri':self.callback_url,
                }
        url = self.AUTH_URL+"?"+urllib.parse.urlencode(params)
        return url

    def get_access_token_by_code(self,code):
        print(code)
        params={
                 'client_id':self.client_id,
                 'client_secret':self.client_secret,
                 'grant_type':code,
                 'redirect_uri':self.callback_url,
                    }
        
        rsp = self.do_post(self.TOKEN_URL,params)
        print(rsp)

        try:
           obj = json.loads(rsp) 
           self.access_token = str(obj['access_token'])
           self.openid = str(obj['uid'])
           return self.get_oauth_userinfo()
        except:
           return None

    def get_oauth_userinfo(self):
        if not self.is_authorized:
            return None
        params ={'uid':self.openid,'access_token':self.access_token}

        rsp =self.do_get(self.API_URL,params)
        try:
            datas = json.loads(rsp)
            user = OAuthUser()
            user.picture  = datas['avatar_large']
            user.nikename = datas['screen_name']
            user.openid = datas['id']
            user.type = 'weibo'
            user.token = self.access_token
            if 'email' in datas and datas['email']:
                user.email = datas['email']
            return user
        except:
            logger.info('weibo oauth error rsp'+rsp)
            return None


class GoogleOauthManager(BaseOauthManager):
    AUTH_URL ='https://accounts.google.com/o/oauth2/v2/auth'
    TOKEN_URL ='https://www.google.com/oauth2/v4/token'
    API_URL= 'https://www.googleapis.com/oauth2/v3/userinfo'
    ICON_NAME ='google'

    def __init__(self,access_token=None,openid=None):
        self.client_id  = settings.OAHUTH['google']['appkey']
        self.client_secret = settings.OAHUTH['google']['appsecret']
        self.callback_url = settings.OAHUTH['google']['callbackurl']
        super(GoogleOauthManager,self).__init__(access_token = access_token,openid=openid)

    
    def get_authorization_url(self):
        params ={
                'client_id':self.client_id,
                'response_type':'code',
                'redirect_uri':self.callback_url,
                'scope':'openid email',
                }
        url = self.AUTH_URL +"?"+urllib.parse.urlencode(params)
        return url

    def get_access_token_by_code(self,code):
        params  ={
                'client_id':self.client_id,
                'client_secret':self.client_secret,
                'grant_type':'authorization_code',
                'code':code,
                'redirect_uri':self.callback_url
                }

        rsp = self.do_post(self.TOKEN_URL,params)
        print(rsp)
        obj = json.loads(rsp)
        try:
            self.access_token = str(obj['access_token'])
            self.openid=str(obj['id_token'])
            logger.info(self.ICON_NAME+' oauth '+ rsp)
            return self.access_token
        except:
            logger.info(self.ICON_NAME + ' oauth error '+ rsp)
            return None

    def get_oauth_userinfo(self):
        if not self.is_authorized:
            return None
        params = {
                'access_token':self.access_token
                }

        rsp = self.do_get(self.API_URL,params)
        print(rsp)
        try:
            datas = json.loads(rsp)
            user = OAuthUser()
            user.picture = datas['picture']
            user.nikename = datas['name']
            user.openid = datas['sub']
            user.type = 'google'
            user.token = self.access_token
            if datas['email']:
                user.email = datas['email']
            return user    
        except:
            logger.info('google oauth error.rsp'+rsp)
            return None

class GitHubOauthManager(BaseOauthManager):
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    TOKEN_URL = 'https://github.com/login/oauth/access_token'
    API_URL = 'https://api.github.com/user'
    ICON_NAME = 'github'

    def __init__(self, access_token=None, openid=None):
        self.client_id = settings.OAHUTH['github']['appkey']
        self.client_secret = settings.OAHUTH['github']['appsecret']
        self.callback_url = settings.OAHUTH['github']['callbackurl']
        super(GitHubOauthManager, self).__init__(access_token=access_token, openid=openid)

    def get_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.callback_url,
            'scope': 'user',
        }
        url = self.AUTH_URL + "?" + urllib.parse.urlencode(params)
        return url

    def get_access_token_by_code(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.callback_url
        }
        rsp = self.do_post(self.TOKEN_URL, params)
        print(rsp)
        try:
            from urllib import parse
            r = parse.parse_qs(rsp)
            self.access_token = (r['access_token'][0])
            return self.access_token
        except:
            return None

    def get_oauth_userinfo(self):
        if not self.is_authorized:
            return None
        params = {
            'access_token': self.access_token
        }
        rsp = self.do_get(self.API_URL, params)
        print(rsp)
        try:
            datas = json.loads(rsp)
            user = OAuthUser()
            user.picture  = datas['avatar_url']
            user.nickname  = datas['name']
            user.openid  =datas['id']
            user.type = 'gitbub'
            user.token = self.access_token
            if datas['email']:
                user.email = datas['email']

            return user
        except:
            logger.info('github oauth error .rsp'+rsp)
            return None

    
def  get_oauth_apps():
    applications = BaseOauthManager.__subclasses__()
    return list(map(lambda x:x(),applications))

def get_manager_by_type(type):
    apllications = get_oauth_apps()
    finds = list(filter(lambda x:x.ICON_NAME.lower() == type.lower(),applications))
    if finds:
        return finds[0]
    return None
