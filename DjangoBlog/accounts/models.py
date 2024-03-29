from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
from django.urls import reverse
from django.contrib.sites.models import Site
#创建用户管理模型
"""
class BlogUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        user = self.model(username=username,email=email,nickname=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
"""        
#创建用户模型
class BlogUser(AbstractUser):
    nickname = models.CharField('昵称',max_length = 50,blank = True)
    mugshot = models.ImageField('头像',upload_to = 'upload/mugshots',blank =True)
    #objects = BlogUserManager()

    def get_absolute_url(self):
        return reverse('blog:author_detail',kwargs={'author_name':self.username})

    def __str__(self):
        return self.email
    
    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = "https://{site}{path}".format(site=site,path=self.get_absolute_url())
        return url

