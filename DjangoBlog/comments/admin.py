from django.contrib import admin

# Register your models here.
#注册模型
from .models import Comment
admin.site.register(Comment)
