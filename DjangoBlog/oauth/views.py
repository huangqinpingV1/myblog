from django.shortcuts import render
from .oauthmanager import WBOauthManager,GoogleOauthManager
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import GoogleUserInfo


# Create your views here.


def wbauthorize(self,sitename):
    manager = WBOauthManager(client_id = settings.OAHUTH['sina']['appkey'],
            client_secret=settings.OAUTH['sina']['appsecret'],
            callback_url=settings.OAUTH['sina']['callbackurl'])

    code = request.GET.get('code',None)
    rsp = manager.get_access_token_by_code(code)
    print(rsp)
    return HttpResponse(rsp)


def wboauthurl(requst):
    manager  =WBOauthManager(client_id=settings.OAUTH['sina']['appkey'],
            client_secret=settings.OAHUTH['sina']['appsecret'],
            callback_url=settings.OAUTH['sina']['callbackurl'])

    url = manager.get_authorization_url()
    return HttpResponse(url)


def googleoauthurl(request):
    manager = GoogleOauthManager(client_id=settings.OAUTH['google']['appkey'],
            client_secret=settings.OAUTH['google']['appsecret'],
            callback_url=settings.OAUTH['google']['callbackurl'])

    url = manager.get_authorization_url()
    return HttpResponse(url)


def googleauthorize(request):
     manager = GoogleOauthManager(client_id=settings.OAUTH['google']['appkey'],
            client_secret=settings.OAUTH['google']['appsecret'],
            callback_url=settings.OAUTH['google']['callbackurl'])

     code = request.GET.get('code',None)
     rsp  = manager.get_access_token_by_code(code)
     print(rsp)
     user = manager.get_oauth_userinfo()
     if user:
         email = user['email']
         author = get_user_model().objects.get(email=email)
         if not author:
             author = get_user_model().objects.create_user(username=user["name"],
                     email  =email,password = None,nikename=user['name'])
         if not GoogleUserInfo.objects.filter(author_id=author.pk):
             userinfo = GoogleUserInfo()
             userinfo.author =author
             userinfo.picture  = user['picture']
             userinfo.token = manager.access_token
             userinfo.openid = manager.openid
             userinfo.nikename =user['name']
             userinfo.save()

     return HttpResponse(rsp)        



