from django import template
from ..models import Products, Comments


# 对于经常需要从数据库获取的数据，自定义一些标签方便在模板中使用
register = template.Library()


# 最新产品
@register.simple_tag
def get_recent_products(num: int=4):
    return Products.objects.all().order_by('-pub_date')[:num]


# 最热门产品
@register.simple_tag
def get_hot_products(num: int=4):
    return Products.objects.all().order_by('comments_count')[:num]


# 分类
@register.simple_tag
def category():
    return Products.objects.values(
        'category', 
        'category_en'
    ).order_by('category').distinct()