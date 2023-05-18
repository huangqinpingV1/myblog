from django.shortcuts import render

# Create your views here.
from .models import Comment
from blog.models import Article
from .forms import CommentForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from accounts.models import BlogUser
from django import forms
from django.contrib import auth

class CommentPostView(FormView):
    form_class = CommentForm
    template_name ='blog/article_detail.html'
    
    def get(self,request,*args,**kwargs):
        article_id = self.kwargs['article_id']
        article  = Article.objects.get(pk=article_id)
        url = article.get_absolute_url()
        print("文章路径url="+url)
        return HttpResponseRedirect(url + "#comments")


    def form_invalid(self,form):
        article_id  = self.kwargs['article_id']
        article = Article.objects.get(pk = article_id)
        u = self.request.user

        if self.request.user.is_authenticated:
            form.fields.update({'email':forms.CharField(widget=forms.HiddenInput()),'name':forms.CharField(widget=forms.HiddenInput())})
            user =self.request.user
            form.fields['email'].initial = user.email
            form.fields['name'].initial = user.username

        return self.render_to_response({'form':form,'article':article})

    def form_valid(self,form):
        """提交的数据验证合法后的逻辑"""
        user = self.request.user
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)

        if not self.request.user.is_authenticated():
            comment = form.save(False)
            comment.article = article
            user = get_user_model().objects.get_or_create(username=username,email=email)[0]

        commant = form.save(False)
        comment.article = article
        comment.author = user
        
        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(pk  = form.cleaned_data['parent_comment_id'])
            comment.parent_comment  = parent_comment

        comment.save(True)

        from DjangoBlog.utils import expire_view_cache,cache
        from django.contrib.sites.models import Site
        path = article.get_absolute_url()
        site = Site.objects.get_current().domain

        expire_view_cache(path,servername=site,serverport=self.request.get_port(),key_prefix='blogdetail')
        if cache.get('seo_processor'):
            cache.delete('seo_processor')

        return HttpResponseRedirect("%s#div-comment-%d" % (article.get_absolute_url(),comment.pk))



