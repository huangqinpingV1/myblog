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

class CommentPostView(FormView):
    form_class = CommentForm
    template_name ='blog/articledetail.html'
    
    def get(self,request,*args,**kwargs):
        article_id = self.kwargs['article_id']
        url = reverse('blog:detail',kwargs ={'article_id':article_id})
        return HttpResponseRedirect(url)


    def form_invalid(self,form):
        article_id  = self.kwargs['article_id']
        article = Article.objects.get(pk = article_id)

        return self.render_to_response({'form':form,'article':article})

    def form_valid(self,form):
        """提交的数据验证合法后的逻辑"""
        user = self.request.user
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)

        if not self.request.user.is_authenticated():
            comment = form.save(False)
            comment.article = article
            user = get_user_model().objects.create_user(username=username,email=email,password = None)
        
        author_id = user.pk


        comment.author = get_user_mpdel().objects.get(pk=author_id)
        
        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(pk  = form.cleaned_data['parent_comment_id'])
            comment.parent_comment  = parent_comment

        comment.save(True)

        return HttpResponseRedirect("%s#div-comment-%d" % (article.get_absolute_url(),comment.pk))



