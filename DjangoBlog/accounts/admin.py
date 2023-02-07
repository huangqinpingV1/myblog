from django.contrib import admin
from .models import BlogUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
#注册模型
admin.site.register(BlogUser,UserAdmin)

