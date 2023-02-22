from django.urls import path
from . import views
#如果引用blog的url使用的include中指定了namespace则必须定义app_name或者在include中指定app_name
app_name ='blog'
urlpatterns  =[
    path(r'',views.IndexView.as_view(),name='index'),
    #path(r'article/<article_id>',views.ArticleDetailView.as_view(),name='detail'),
    path('<year>/<month>/<day>/<article_id>-<slug>.html',views.ArticleDetailView.as_view()),
    path(r'category/<category_name>',views.CategoryDetailView.as_view(),name ='category_detail'),
    path(r'author/<author_name>',views.AuthorDetailView.as_view(),name='author_detail'),
    path(r'tags/<tag_name>',views.TagDetailView.as_view(),name='tag_detail'),
    ]
