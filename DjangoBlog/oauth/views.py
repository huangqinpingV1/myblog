from django.shortcuts import render
from .oauthmanager import WBOauthManager
from django.conf import settings
from django.http import HttpResponse

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


