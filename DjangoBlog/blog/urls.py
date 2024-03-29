from django.urls import path
from . import views
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from django.views.decorators.cache import cache_page

#如果引用blog的url使用的include中指定了namespace则必须定义app_name或者在include中指定app_name
app_name ='blog'
urlpatterns  =[
    path('',views.IndexView.as_view(),name='index'),
    path('page/<page>',views.IndexView.as_view(),name='index_page'),
    path('article/<year>/<month>/<day>/<article_id>-<slug>.html',views.ArticleDetailView.as_view(),name = 'detailbyid'),
    path('category/<category_name>',views.CategoryDetailView.as_view(),name ='category_detail'),
    path('author/<author_name>',views.AuthorDetailView.as_view(),name='author_detail'),
    path('tags/<tag_name>',views.TagDetailView.as_view(),name='tag_detail'),
    path('blogpage/<year>/<month>/<day>/<page_id>-<slug>.html',views.ArticleDetailView.as_view(),name ='pagedetail'),
    path('upload',views.fileupload,name='upload'),
    path('refresh',views.refresh_memcache,name='refresh')
    ]

