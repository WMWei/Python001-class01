from django.db import models

class Comments(models.Model):
    id = models.IntegerField(
        primary_key=True,
        
        verbose_name='id',
    )
    cid = models.CharField(
        max_length=20,
        verbose_name='评论id',
    )
    user_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='用户名',
    )
    rate = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='评分',
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='评论',
    )
    date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='发布日期',
    )
    # 外键，关联Movie的douban_id
    movie = models.ForeignKey(
        'Movies',
        on_delete=models.CASCADE,
        verbose_name='电影'
    )

    class Meta:
        managed = False
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date']
    
    def __str__(self):
        return (self.cid, self.user_name, self.comment)


class Movies(models.Model):
    movie_id = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name='电影id',
    )
    imdb_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='imdb_id',
    )
    movie_name = models.CharField(
        max_length=100,
        verbose_name='电影名称',
    )
    release_date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='上映日期',
    )
    movie_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='电影类型',
    )
    runtime = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='电影时长',
    )
    area = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='区域',
    )
    language = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name='语言',
    )
    img_src = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='海报',
    )
    rate = models.FloatField(
        blank=True,
        null=True,
        verbose_name='评分',
    )
    rate_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='评价人数',
    )
    indent = models.TextField(
        blank=True,
        null=True,
        verbose_name='简介',
    )
    link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='页面链接',
    )

    class Meta:
        managed = False
        db_table = 'movies'
        verbose_name = '电影'
        verbose_name_plural = verbose_name
        ordering = ['-rate']
