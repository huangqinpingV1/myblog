from django.contrib import admin
from .models import OAuthUser
# Register your models here.

class OAuthUserAdmin(admin.ModelAdmin):
    list_display = ('id','author','nikename','type','picture','email',)
    list_display_links = ('id','nikename')
    list_filter =('author','type',)


admin.site.register(OAuthUser,OAuthUserAdmin)    
