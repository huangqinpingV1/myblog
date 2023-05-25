from django.contrib import admin
from .models import Article,Category,Tag,Links
from pagedown.widgets import AdminPagedownWidget
from django import forms
from django.utils.translation import  gettext_lazy as _

class ArticleListFilter(admin.SimpleListFilter):
    title = _("作者")
    parameter_name = 'author'


    def lookups(self,request,model_admin):
        authors  = list(map(lambda x: x.author,Article.objects.all()))
        for author in authors:
            yield (author.id,_(author.name))
    
    def queryset(self,request,queryset):
        id = self.value()
        if id:
            return queryset.filter(author__id__exact=id)
        else:
            return queryset

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget  = AdminPagedownWidget())

    class Meta:
        model = Article
        fields ='__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    list_display = ('id','title','author','created_time','views','status','type')
    list_display_links =('id','title')
    list_filter =  (ArticleListFilter,'status','type','category','tags')
    filter_horizontal = ('tags',)
    exclude  = ('slug','created_time')


    def save_model(self,request,obj,form,change):
        super(ArticleAdmin,self).save_model(request,obj,form,change)
        from DjangoBlog.utils import cache
        cache.clear()

class TagAdmin(admin.ModelAdmin):
    exclude = ('slug',)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)
# Register your models here.
#注册模型
admin.site.register(Article,ArticleAdmin)
#admin.site.register(BlogPage,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Links)
