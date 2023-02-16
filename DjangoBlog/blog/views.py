from django.shortcuts import render
from blog.models import Article,Category,Tag
# Create your views here.
#View 视图主要使用Model 的模型
from django.views.generic.list import  ListView
from django.views.generic.detail import DetailView
from django.conf import settings
#markdown编辑器包
import markdown
#通用显示视图
#调试调用栈
import traceback
class ArticleListView(ListView):
    #template_name 属性用于指定用哪个模板进行渲染
    template_name = 'blog/index.html'
    #context_object_name 用于给上下文变量取名（模板中使用）
    context_object_name   = 'article_list'
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
    template_name =  'blog/articledetail.html'
    model = Article
    pk_url_kwarg = 'article_id'
    context_object_name  = "article"

    def get_object(self):
        print("ArticleDetailView get_object() enter")
        obj = super(ArticleDetailView,self).get_object()
        obj.viewed()
        return obj

class CategoryDetailView(ArticleListView):
    print("CategoryDetailView constructor")
    
    def get_queryset(self):
        categoryname  = self.kwargs['category_name']
        print("CateGoryDetailView get_queryset() enter")
        self.page_description ='分类目录归档:·%s·' % categoryname
        article_list = Article.objects.filter(category__name=categoryname,status='p')
        return article_list
    
    def get_context_data(self,**kwargs):
        #增加额外数据
        print("CategoyDetailView get_context_data() enter")
        kwargs['page_description'] = self.page_description
        return super(CategoryDetailView,self).get_context_data(**kwargs)

class AuthorDetailView(ArticleListView):
    print("AuthorDetailView constructor")
    def get_queryset(self):
        print("AuthorDetailView get_queryset()")
        author_name = self.kwargs['author_name']
        self.page_description ='分类目录归档:·%s·' % author_name
        article_list = Article.objects.filter(author__username=author_name)
        return article_list
    
    def get_context_data(self,**kwargs):
        kwargs['page_description'] = self.page_description
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
    print("TagDetailView constrouctor")
    def get_queryset(self):
        print("TagDetailView get_queryset() enter")
        tag_name = self.kwargs['tag_name']
        self.page_description = '分类标签: %s '% tag_name
        article_list = Article.objects.filter(tags__name = tag_name)
        return article_list

def get_context_data(self,**kwargs):
    print("TagDetailView get_context_data()")
    kwargs['page_description'] = self.page_description
    return super(TagDetailView,self).get_context_data(**kwargs)


class MystView():
    print("MyTestView constructor")
