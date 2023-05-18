from django.contrib import admin
from .models import Article,Category,Tag,Links
from pagedown.widgets import AdminPagedownWidget
from django import forms

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget  = AdminPagedownWidget())

    class Meta:
        model = Article
        fields ='__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

    def save_model(self,request,obj,form,change):
        super(ArticleAdmin,self).save_model(request,obj,form,change)
        from DjangoBlog.utils import cache
        cache.clear()

# Register your models here.
#注册模型
admin.site.register(Article,ArticleAdmin)
#admin.site.register(BlogPage,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Links)
