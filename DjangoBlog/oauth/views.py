from django.shortcuts import render
from .oauthmanager import WBOauthManager,GoogleOauthManager,get_manager_by_type
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import oauthuser
from django.contrib.auth import login


# Create your views here.

def authorize(request):
    manager  = None
    type = request.GET.get('type',None)
    
    if not type:
        return HttpResponseRedirect('/')
    manager = get_manager_by_type(type)
    if not manager:
        return HttpResponseRedirect('/')

    code = request.GET.get('code',None)
    rsp = manager.get_access_token_by_code(code)
    if not rsp:
        return HttpResponseReirect(manager.get_authorization_url())
    user = manager.get_oauth_userinfo()
    author = None

    if user:
        email = user.email
        if email:
            author = get_user_model().objects.get(email=email)
            if not author:
                #不存在则创建
                author = get_user_model().objects.create_user(username= user["name"],email=email)
            user.author = author
            user.save()
            login(requset,author)
            return HttpResponseRedirect('/')
        if not email:
            author = get_user_model().objects.create_user(username=user['name'],email=email)


"""
def wbauthorize(self,sitename):
    manager = WBOauthManager()

    code = request.GET.get('code',None)
    rsp = manager.get_access_token_by_code(code)
    print(rsp)
    return HttpResponse(rsp)


def wboauthurl(requst):
    manager  =WBOauthManager()

    url = manager.get_authorization_url()
    return HttpResponse(url)


def googleoauthurl(request):
    manager = GoogleOauthManager()

    url = manager.get_authorization_url()
    return HttpResponse(url)


def googleauthorize(request):
     manager = GoogleOauthManager()

     code = request.GET.get('code',None)
     rsp  = manager.get_access_token_by_code(code)
     print(rsp)
     user = manager.get_oauth_userinfo()
     if not rsp:
         return HttpResponseRedirect(manager.get_authorization_url())
     if user:
         email = user['email']
         if email:
             author = get_user_model().objects.get(email=email)
             if not author:
                author = get_user_model().objects.create_user(username=user["name"],email  =email,password = None,nikename=user['name'])
             if not GoogleUserInfo.objects.filter(author_id=author.pk):
                 userinfo = GoogleUserInfo()
                 userinfo.author =author
                 userinfo.picture  = user['picture']
                 userinfo.token = manager.access_token
                 userinfo.openid = manager.openid
                 userinfo.nikename =user['name']
                 userinfo.save()
             loggin(request,author)
     return HttpResponseRedirect('/')       


"""
