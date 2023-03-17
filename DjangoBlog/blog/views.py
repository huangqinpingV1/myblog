from django.shortcuts import render
from blog.models import Article,Category,Tag
# Create your views here.
#View 视图主要使用Model 的模型
from django.views.generic.list import  ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
#通用显示视图
#调试调用栈
import traceback
#评论相关
from django.views.generic import UpdateView
from comments.forms import CommentForm
from comments.models import Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.conf import settings
from django import forms
from abc import ABCMeta,abstractmethod
from haystack.generic_views import SearchView
from blog.forms import BlogSearchForm
import datetime
from django.views.decorators.csrf import csrf_exempt
import os
"""class SeoProcessor():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_title(self):
        pass
    
    @abstractmethod
    def get_keywords(self):
        pass

    @abstractmethod
    def get_description(self):
        pass
"""

class ArticleListView(ListView):
    #template_name 属性用于指定用哪个模板进行渲染
    template_name = 'blog/article_index.html'
    #context_object_name 用于给上下文变量取名（模板中使用）
    context_object_name   = 'article_list'
    #页面类型
    page_type =  ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg ='page'
    print("ArticleListView() constructor")
    
    
    def __init__(self):
        print("ArtilceListView() __init__()")
        self.page_description =  ''

class IndexView(ArticleListView):
    print("Index() constructor")
    #template_name属性用于指定用哪个模板进行渲染
    #template_name = 'index.html'


    #context_object_name属性用于给上下文变量取名（在模板中使用该名字)
    #context_object_name = 'article_list'


    #get_queryset是覆盖ListView的方法,由父类调用
    def get_queryset(self):
        print("IndexView get_queryset() enter")
        article_list = Article.objects.filter(status='p')
        #for article in article_list:
        #    article.body = article.body[0:settings.ARTICLE_SUB_LENGTH]

        return article_list
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print("get_context_data() enter")
        return context

class ArticleDetailView(DetailView):
    print("ArticleDetailView() enter")
    template_name =  'blog/article_detail.html'
    model = Article
    pk_url_kwarg = 'article_id'
    context_object_name  = "article"

    def get_object(self):
        print("ArticleDetailView get_object() enter")
        obj = super(ArticleDetailView,self).get_object()
        obj.viewed()
        return obj

    #重写get_context_data
    def get_context_data(self,**kwargs):
        artilceid = int(self.kwargs[self.pk_url_kwarg])
        
        def get_article(id):
            try:
                return Article.objects.get(pk = id)
            except ObjectDoesNotExist:
                return None
        #评论相关
        comment_form = CommentForm()
        u = self.request.user
        if self.request.user.is_authenticated:
            comment_form.fields.update({'email':forms.CharField(widget=forms.HiddenInput()),'name':forms.CharField(widget=forms.HiddenInput()),})
            user = self.requst.user
            comment_form.fields['email'].initial  = user.email
            comment_form.fields['name'].initial  = user.username
        
        article_comments = self.object.comment_set.all()
        print(article_comments)

        kwargs['form']  = comment_form
        kwargs['article_comments'] = article_comments
        kwargs['comment_count'] = len(article_comments) if article_comments else 0;
        #评论相关
        next_article =  get_article(article+1)
        pre_article = get_article(article -1)
        kwargs['next_article']  = next_article
        kwargs['pre_article'] = pre_article

        return super(ArticleDetail,self).get_context_data(**kwargs)

class CategoryDetailView(ArticleListView):
    print("CategoryDetailView constructor")
    page_type  ="分类目录归档"
    
    def get_queryset(self):
        categoryname  = self.kwargs['category_name']
        print("CateGoryDetailView get_queryset() enter")
        try:
            categoryname = categoryname.split('/')[-1]
        except:
            pass
        article_list = Article.objects.filter(category__name=categoryname,status='p')
        return article_list
    
    def get_context_data(self,**kwargs):
        #增加额外数据
        print("CategoyDetailView get_context_data() enter")
        categoryname = self.kwargs['category_name']
        try:
            categoryname = categoryname.split('/')[-1]
        except:
            pass
        kwargs['page_type'] =CategoryDetailView.page_type
        kwargs['tag_name'] = categoryname
        return super(CategoryDetailView,self).get_context_data(**kwargs)

class AuthorDetailView(ArticleListView):
    page_type = '作者文章归档'
    print("AuthorDetailView constructor")

    def get_queryset(self):
        print("AuthorDetailView get_queryset()")
        author_name = self.kwargs['author_name']
        article_list = Article.objects.filter(author__username=author_name)
        return article_list
    
    def get_context_data(self,**kwargs):
        author_name = self.kwargs['author_name']
        kwargs['page_type'] =AuthorDetailView.page_type
        kwargs['tag_name'] = author_name
        return super(AuthorDetailView,self).get_context_data(**kwargs)

class TagListView(ListView):
    print("TagListView constructor")
    template_name = ''
    context_object_name =  'tag_list'

    def get_queryset(self):
        print("TagListView get_query_set() enter")
        tags_list = []
        tags = Tag.objects.all()
        for t in tags:
            t.article_set.count()

class TagDetailView(ArticleListView):
    page_type ='分类标签归档'
    print("TagDetailView constrouctor")
    def get_queryset(self):
        print("TagDetailView get_queryset() enter")
        tag_name = self.kwargs['tag_name']
        article_list = Article.objects.filter(tags__name = tag_name)
        return article_list

def get_context_data(self,**kwargs):
    print("TagDetailView get_context_data()")
    tag_name = self.kwargs['tag_name']
    kwargs['page_type'] = TagDetailView.page_type
    kwargs['tag_name'] = tag_name
    return super(TagDetailView,self).get_context_data(**kwargs)


#文件上传功能
@csrf_exempt
def fileupload(request):
    if request.method == 'POST':
        fname =''
        timestr = datetime.datetime.now().strftime("%Y/%m/%d")
        basepath = os.path.join(r'/var/www/resource/image/',timestr)
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        for filename ,file in request.FILES.iteritems():
            fname = filename
            savepath = os.path.join(basepath,filename)
            with open(savepath,"wb+") as wfile:
                for chunk in file.chunks():
                    wfile.write(chunk)
        
        return HttpResponse('http://1.12.250.75/'+'image/'+timestr+'/' + fname)
     
    else:
        return HttpResponse("only for post")

class MystView():
    print("MyTestView constructor")
