from django import template
from django.db.models import Count
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
    return Products.objects.annotate(
        Count('comments')
    ).order_by('-comments__count')[:num]


# 获取分类
@register.simple_tag
def product_category():
    return Products.get_category()


# 最新/最热标签
@register.simple_tag
def home_sub_category():
    return {
        'new': '最新',
        'hot': '最热',
    }