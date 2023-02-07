from django.contrib import admin
from .models import Article,Category,Tag
# Register your models here.
#注册模型
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
