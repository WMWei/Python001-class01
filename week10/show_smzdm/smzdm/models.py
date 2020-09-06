from datetime import tzinfo
from django.db import models
from django.utils import timezone


class Comments(models.Model):
    cid = models.CharField(
        unique=True, 
        max_length=20,
        verbose_name='评论id',
    )
    uid = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='用户id',
    )
    username = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='用户名',
    )
    comment = models.TextField(
        blank=True, 
        null=True,
        verbose_name='评论',
    )
    pub_date = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name='发布时间',
    )
    avatar = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='头像',
    )
    sentiments = models.FloatField(
        blank=True, 
        null=True,
        verbose_name='情感分析',
    )

    parent_cid = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        to_field='cid',
        db_column='parent_cid', 
        # related_name='sub_comments',
        blank=True, 
        null=True,
        verbose_name='回复评论',
    )
    pid = models.ForeignKey(
        'Products', 
        on_delete=models.CASCADE, 
        to_field='pid',
        db_column='pid',
        # related_name='comments',
        verbose_name='产品id',
    )

    class Meta:
        managed = False
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-pub_date']
    
    @property
    def local_pub_date(self):
        # 解决Django从数据库读取时间，无论数据库时区为何，总是默认为UTC的问题
        return self.pub_date.replace(tzinfo=timezone.get_current_timezone())
    
    def __str__(self):
        return f'{self.cid}, {self.username}, {self.comment}'


class Products(models.Model):
    pid = models.CharField(
        unique=True, 
        max_length=20,
        verbose_name='产品id',
    )
    price = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='价格',
    )
    title = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='产品',
    )
    pub_date = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name='发布时间',
    )
    category = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='分类',
    )
    category_en = models.CharField(
        max_length=40, 
        blank=True, 
        null=True,
        verbose_name='category',
    )
    price_from = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='产品来源',
    )
    img = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='产品图片',
    )
    link = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='链接',
    )

    class Meta:
        managed = False
        db_table = 'products'
        verbose_name = '产品'
        verbose_name_plural = verbose_name
        ordering = ['-pub_date']
    
    @property
    def local_pub_date(self):
        # 解决Django从数据库读取时间，无论数据库时区为何，总是默认为UTC的问题
        return self.pub_date.replace(tzinfo=timezone.get_current_timezone())

    @classmethod
    def get_category(cls):
        return cls.objects.values(
            'category_en',
            'category'
        ).order_by('category_en').distinct()

    def __str__(self):
        return f'{self.pid}, {self.title}, {self.price}'
