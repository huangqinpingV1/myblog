from django.db import models
from django.conf import settings
from blog.models import Article
# Create your models here.
#创建评论模型
class Comment(models.Model):
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add = True)
    last_mod_time = models.DateTimeField('修改时间',auto_now = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '作者',on_delete=models.CASCADE)

    article = models.ForeignKey(Article,verbose_name='文章',on_delete = models.CASCADE)
    parent_comment = models.ForeignKey('self',verbose_name='上级评论',blank= True,null = True,on_delete=models.CASCADE)


    class Meta:
        ordering = ['created_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body

