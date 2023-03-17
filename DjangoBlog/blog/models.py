from django.db import models
#路由相关和设置相关包
from django.urls import reverse
from django.conf import settings
from uuslug import slugify
# Create your models here.
#文章模型
class Article(models.Model):
    """文章"""
    STATUS_CHOICES =(('d','草稿'),('p','发表'))
    COMMENT_STATUS =(('o',"打开"),('c','关闭'))
    TYPE =(('a','文章'),('p','页面'))

    title = models.CharField('标题',max_length=200)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add = True)
    last_mod_time = models.DateTimeField('修改时间',auto_now = True)
    pub_time  = models.DateTimeField('发布时间',blank=True,null=True,help_text='不指定发布时间则视为草稿，可以指定未来时间，到时将自动发布。')
    status  = models.CharField('文章状态',max_length=1,choices=STATUS_CHOICES,default ='p')
    comment_status  = models.CharField('评论状态',max_length=1,choices=COMMENT_STATUS,default='o')

    views  = models.PositiveIntegerField('浏览量',default  = 0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '作者',on_delete=models.CASCADE)

    category = models.ForeignKey('Category',verbose_name='分类',on_delete=models.CASCADE,blank  = True,null =True)
    tags  = models.ManyToManyField('Tag',verbose_name='标签集合',blank=True)

    slug = models.SlugField(default='no-slug',max_length=60,blank=True)
    type =models.CharField('类型',max_length=1,choices = TYPE,default = 'a')



    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-pub_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'article_id':self.pk,
            'year':self.created_time.year,
            'month':self.created_time.month,
            'day':self.created_time.day,
            'slug':self.slug})

    def get_category_tree(self):
        names =[]

        #递归调用
        def parse(category):
            names.append((category.name, category.get_absolute_url()))
            if category.parent_category:
                parse(category.parent_category)
        parse(self.category)
        return names

    def save(self,*args,**kwargs):
        #self.summary = self.summary or self.body[:settings.ARTICLE_SUB_LENGTH]
        if not self.slug or self.slug== 'no-slug' or not self.id:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)


    #浏览量计算
    def viewed(self):
        self.views +=1
        self.save(update_fields =['views'])

    def  comment_list(self):
        comment = self.comment_set.all()
        parent_comments  = comments.filter(parent_comment  = None)

    def get_admin_url(self):
        info = (self._meta.app_label,self._meta.model_name)
        return reverse("admin:%s_%s_change" % info,args=(self.pk,))
#文章分类模型
class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名',max_length =30)
    created_time = models.DateTimeField('创建时间',auto_now_add = True)
    last_mod_time  = models.DateTimeField('修改时间',auto_now = True)
    #增加parent_category字段
    parent_category = models.ForeignKey('self',verbose_name="父级分类",blank  = True,null = True,on_delete=models.CASCADE)


    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:category_detail',kwargs  ={'category_name':self.name})
    
    def __str__(self):
        return self.name

#文章标签模型 
class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名',max_length=30)
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
       return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail',kwargs={'tag_name':self.name})

    def get_article_count(self):
        return Article.objects.filter(tags__name = self.name).distinct().count()

    class Meta:
        ordering =  ['name']
        verbose_name = "标签"
        verbose_name_plural  = verbose_name

class Links(models.Model):
    """友情链接"""
    name = models.CharField("链接名称",max_length=30)
    link = models.URLField("链接地址")
    sequence = models.IntegerField("排序",unique = True)
    created_time = models.DateTimeField('创建时间',auto_now_add = True)
    last_mod_time = models.DateTimeField('修改时间',auto_now = True)

    class Meta:
        ordering = ['sequence']
        verbose_name ='友情链接'
        verbose_name_plural  = verbose_name

    def __str__(self):
        return self.name

"""
class BlogPage(models.Model):
    STATUS_CHOICES  =(
            ('d','草稿'),
            ('p','发表'),
            )
    COMMENT_STATUS =(
            ('o','打开'),
            ('c','关闭'),)

    #模型字段
    title = models.CharField('标题',max_length  = 200)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add = True)
    last_mod_time = models.DateTimeField('修改时间',auto_now  = True)
    pub_time = models.DateTimeField('发布时间',blank = True,null = True,help_text="不指定发布时间则为草稿，可以指定未来时间，到时将自动发布。")
    status = models.CharField('文章状态',max_length=1,choices  = STATUS_CHOICES,default= 'd')
    comment_status = models.CharField('评论状态',max_length =1,choices = COMMENT_STATUS)
    views = models.PositiveIntegerField('浏览量',default=0)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name ='作者',on_delete = models.CASCADE)
    slug = models.SlugField(default='no-slug',max_length = 60,blank = True)

    class Meta:
        ordering = ['-pub_time']
        verbose_name = '页面'
        verbose_name_plural = verbose_name

    def __str__(self):
         return self.title

    def get_absolute_url(self):
         return reverse('blog:pagedetail',kwargs={
             'page_id':self.id,
             'year':self.created_time.year,
             'month':self.created_time.month,
             'day':self.created_time.day,
             'slug':self.slug,
             })
 
    def save(self,*args,**kwargs):
         if not self.slug or self.slug == 'no-slug' or not self.id:
             self.slug = slugify(self.title)

         super().save(*args,**kwargs)

     
    def viewed(self):
         self.views +=1
         self.save(update_field=['views'])

    def comment_list(self):
        comments = self.comment_set.all()
        parent_comments = comments.filter(parent_comment = None)
"""        
