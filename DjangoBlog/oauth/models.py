from django.db import models
from django.conf import settings
# Create your models here.

class BaseModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='用户',on_delete=models . CASCADE)
    openid  = models.CharField(max_length= 50)
    nikename  = models.CharField(max_length=50,verbose_name='昵称')
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.nikename

    class Meta:
        abstract = True


class SinaWBUserInfo(BaseModel):
    class Meta:
        verbose_name ='新浪微博'
        verbose_name_plural =verbose_name


class QQUserInfo(BaseModel):
    class Meta:
        verbose_name ='QQ'
        verbose_name_plural = verbose_name

        

