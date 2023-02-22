#!/usr/bin/env python
#encoding:utf-8

from abc import ABCMeta,abstractmethod,abstractproperty
import requests
import json
import urllib.parse

class BaseManager(metaclass=ABCMeta):
    """获取用户授权"""
    AUTH_URL = None
    """获取token"""
    TOKEN_URL = None
    """获取用户信息"""
    API_URL = None

    def __init__(self,client_id,client_secret,callback_url,access_token = None,openid =None):
        self.client_id = client_id
        self.client_secret= client_secret
        self.callback_url = callback_url
        self.access_token = access_token
        self.openid = openid

    @property
    def is_access_token_set(self):
        return self.access_token != None

    @property
    def is_authorized(self):
        return self.is_access_token_set and self.access_token != None and self.openid != None

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

class WBOauthManager(BaseManager):
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    API_URL = 'https://api.weibo.com/2/users/show.json'

    def __init__(self,client_id,client_secret,callback_url,access_token=None,openid=None):
        super(WBOauthManager,self).__init(client_id =client_id,client_secret=client_secret,callback_url=callback_url,access_token=access_token,openid=openid)

    
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
        obj =json.loads(rsp)

        try:
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
        print(rsp)



            
