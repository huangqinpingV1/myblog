from django.urls import path
from . import views
from haystack.forms import ModelSearchForm
from hystack.query import SearchQuerySet
from hystack.views import SearchView

#如果引用blog的url使用的include中指定了namespace则必须定义app_name或者在include中指定app_name
app_name ='blog'
urlpatterns  =[
    path('',views.IndexView.as_view(),name='index'),
    path('page/<page>',views.IndexView.as_view(),name='index_page'),
    #path(r'article/<article_id>',views.ArticleDetailView.as_view(),name='detail'),
    path('article/<year>/<month>/<day>/<article_id>-<slug>.html',views.ArticleDetailView.as_view(),name = 'detail'),
    path('category/<category_name>',views.CategoryDetailView.as_view(),name ='category_detail'),
    path('author/<author_name>',views.AuthorDetailView.as_view(),name='author_detail'),
    path('tags/<tag_name>',views.TagDetailView.as_view(),name='tag_detail'),
    path('blogpage/<year>/<month>/<day>/<page_id>-<slug>.html',views.ArticleDetailView.as_view(),name ='pagedetail'),
    #搜索相关路由
    #path(r'search/',views.BlogSearchView.as_view(),name='search_view')
    ]

