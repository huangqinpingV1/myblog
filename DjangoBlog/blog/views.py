from django.shortcuts import render
from blog.models import Article,Category,Tag
# Create your views here.
#View 视图主要使用Model 的模型
from django.views.generic.list import  ListView
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
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
from django.contrib.auth.decorators import login_required
from DjangoBlog.utils import cache,cache_decorator,logger,get_md5
from django.utils.cache import get_cache_key
from django.utils.decorators import method_decorator
from django.utils.decorators import classonlymethod
from django.http import HttpResponseRedirect
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
"""class CacheTemplateView(ListView):
    @classonlymethod
    def as_view(cls,**initkwargs):
        view = super(CacheTemplateView,cls).as_view(**initkwargs)
        return cache_page(60*60*10)(view)
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
    
    def get_view_cache_key(self):
        return self.request.get['pages']

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset_cache_key(self):
        """
        子类重写，获得queryset的缓存key
        """
        raise  NotImplementedError()
    
    def get_queryset_data(self):

        raise NotImplementedError()

    def get_queryset_from_cache(self,cache_key):
        value =cache.get(cache_key)
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        else:
            article_list = self.get_queryset_data()
            cache.set(cache_key,article_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return article_list

    def get_queryset(self):
        key = self.queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value


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
        article_list = Article.objects.filter(type='a',status='p')
        #for article in article_list:0
        #    article.body = article.body[0:settings.ARTICLE_SUB_LENGTH]

        return article_list
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print("get_context_data() enter")
        return context
    
    def get_queryset_data(self):
       article_list = Article.objects.filter(type='a',status='p')
       return article_list

    def get_queryset_cache_key(self):
       cache_key  =  'index_{page}'.format(page=self.page_number)
       return cache_key

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
        self.object = obj
        return obj
    
    def dispatch(self,request,*args,**kwargs):
        slug = self.kwargs['slug'] if 'slug' in self.kwargs else ''
        if slug:
            obj = super(ArticleDetail,self).get_object()
            return HttpResponseRedirect(obj.get_absolute_url)
        else:
            return super(ArticleDetailView,self).dispatch(request,*args,**kwargs)

    #重写get_context_data
    def get_context_data(self,**kwargs):
        artilceid = int(self.kwargs[self.pk_url_kwarg])
        
        #评论相关
        comment_form = CommentForm()
        u = self.request.user
        if self.request.user.is_authenticated:
            comment_form.fields.update({'email':forms.CharField(widget=forms.HiddenInput()),'name':forms.CharField(widget=forms.HiddenInput()),})
            user = self.requst.user
            comment_form.fields['email'].initial  = user.email
            comment_form.fields['name'].initial  = user.username
        key ="article_comment_{}".format(articleid)
        
        article_comments = self.object.comment_list()
        print(article_comments)

        kwargs['form']  = comment_form
        kwargs['article_comments'] = article_comments
        kwargs['comment_count'] = len(article_comments) if article_comments else 0;
        #评论相关
        
        kwargs['next_article']  = self.object.next_article
        kwargs['pre_article'] = self.object.pre_article

        return super(ArticleDetail,self).get_context_data(**kwargs)

class CategoryDetailView(ArticleListView):
    print("CategoryDetailView constructor")
    page_type  ="分类目录归档"
    

    def get_queryset_data(self):
        slug  = self.kwargs['category_name']
        category = get_object_or_404(Category,slug=slug)
        categoryname = category.name
        self.categoryname = categoryname
        categorynames = list(map(lambda c:c.name,category.get_sub_categorys()))
        article_list = Article.objects.filter(category__name__in =categorynames,status='p')
        return article_list

    
    def get_queryset_cache_key(self):
        slug = self.kwargs['category_name']
        category =get_object_or_404(Category,slug=slug)
        categoryname =category.name
        self.categoryname =categoryname
        cache_key ='category_list_{categoryname}_{page}'.format(categoryname=cateforyname,page=self.page_number)
        return cache_key

    def get_queryset(self):
        slug = self.kwargs['category_name']
        category= Category.objects.get(slug=slug)
        categoryname = category.name
        self.categoryname = categoryname
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
        categoryname = self.categoryname
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
    
    def get_queryset_cache_key(self):
        author_name  = self.kwargs['author_name']
        cache_key = 'author_{author_name}_{page}'.fromat(author_name=author_name,page=self.page_number)
        return cache_key

    def get_queryset_data(self):
        print("AuthorDetailView get_queryset_data()")
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
    def get_queryset_data(self):
        print("TagDetailView get_queryset() enter")
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag,slug=slug)
        tag_name = tag.name
        self.name = tag_name
        article_list = Article.objects.filter(tags__name = tag_name)
        return article_list

    def get_queryset_cache_key(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag,slug=slug)
        tag_name = tag.name
        self.name  =tag_name
        cache_key = 'tag_{tag_name}_{page}'.format(tag_name=tag_name,page=self.page_number)
        return cache_key

    def get_context_data(self,**kwargs):
      print("TagDetailView get_context_data()")
      tag_name = self.name
      kwargs['page_type'] = TagDetailView.page_type
      kwargs['tag_name'] = tag_name
      return super(TagDetailView,self).get_context_data(**kwargs)


#文件上传功能
@csrf_exempt
def fileupload(request):
    if request.method == 'POST':
        response =[]
        for filename in request.FILES:    
            timestr = datetime.datetime.now().strftime('%Y/%m/%d')
            imagextensions  = ['jpg','png','jpeg','bmp']
            fname  =  u''.join(str(filename))

            isimage = len([i for i in imagextensions if fname.find(i) >= 0]) >0
            basepath = os.path.join(r'/var/www/resource/image/' + 'files' if not isimage else 'image' +'/',timestr)

            url = 'https://resource.lylinux.net/{type}/{timestr}/{filename}'.format(type='files' if not isimage else 'image' ,timestr=timestr,filename  = filenamme)
            if not os.path.join(basepath):
                os.makedirs(basepath)
            savepath = os.path.join(basepath,filename)
            with open(savepath,"wb+") as wfile:
                for chunk in request.FILES[filename].chunks():
                    wfile.write(chunk)
            
            if isimage:
                from PIL import Image
                image = Image.open(savepath)
                image.save(savepath,quality = 20,optimize = True)
            response.append(url)
        return HttpResponse(response)
     
    else:
        return HttpResponse("only for post")

@login_required
def refresh_memcache(requst):
    try:
        if request.user.is_superuser:
            from DjangoBlog.utils import cache
            if cache and  cache is not None:
                cache.clear()
            return HttpResponse("ok")
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
    except Exception as e:
        return HttpResponse(e)

class MystView():
    print("MyTestView constructor")
