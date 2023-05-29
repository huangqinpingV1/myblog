from django.contrib import admin
from .models import BlogUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
#注册模型
class BlogUserAdmin(UserAdmin):
    list_display=('id','last_login','is_superuser','email','date_joined','username')

admin.site.register(BlogUser,BlogUserAdmin)

