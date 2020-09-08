from django.db.models import Q, Avg
from django.http import JsonResponse
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from .models import Products, Comments
from .encoder import DatetimeJSONEncoder


# 主页
@require_http_methods(['GET'])
def home(request):
    params = request.GET
    sub_cate = params.get('sort', 'new')
    if sub_cate in ('new', 'hot'):
        return render(
            request,
            'home.html',
            context={'sub_cate': sub_cate}
        )
    else:
        return render(
            request,
            '404.html',
            status=404,
        )


# 目录页
@require_http_methods(['GET'])
def index(request, cate=None):
    # localhost:8000/index/?pageNo={}&q={}
    # localhost:8000/index/<str:cate>/?pageNo={}&q={}
    PAGE_SIZE = 4
    params = request.GET
    page_no = params.get('pageNo', 1)
    query_str = params.get('q', '')
    # Q查询数组
    queries = []
    # 分类中文显示
    cate_zh = '全部分类'
    # 先按分类筛选
    if cate:
        try:
            # 判断查询的分类字符串是否存在，并获取对应中文显示用于模板
            cate_zh = Products.get_category().get(category_en=cate).get('category')
            queries.append(Q(category_en=cate))
        except Products.DoesNotExist as _:
            # 对于不存在的页面返回404
            return render(
                request,
                '404.html',
                status=404
            )
    # 再按查询字符串筛选
    if query_str:
        query_str_list = query_str.split('+')
        queries = queries + [
            Q(title__contains=q) | 
            Q(price__contains=q) |
            Q(price_from__contains=q)
            for q in query_str_list if q
        ]
    # 获取查询结果
    all_products = Products.objects.filter(*queries).order_by('-pub_date')
    # 分页
    paginator = Paginator(all_products, PAGE_SIZE)
    try:
        products = paginator.page(page_no)
    except PageNotAnInteger:
        # 对于无法进行数字转换的页码全部处理为1
        # 确保模板使用的page_no是int
        page_no = 1
        products = paginator.page(page_no)
    except EmptyPage:
        # 对于超出的页码，全部处理为末尾页
        products = paginator.page(paginator.num_pages)
    return render(
        request,
        'index.html',
        context={
            'products': products,
            'page_no': int(page_no),
            'paginator': paginator,
            'q': query_str,
            'cate_zh': cate_zh,
        },
    )


# 商品详情页
@require_http_methods(['GET'])
def detail(request, pid):
    try:
        product = Products.objects.get(pid=pid)
    except Products.DoesNotExist as _:
        return render(
            request,
            '404.html',
            status=404
        )
    return render(
        request,
        'detail.html',
        locals()
    )


# 详情评论页/ajax页
@require_http_methods(['GET'])
def comments(request, pid):
    product = get_object_or_404(Products, pid=pid)
    if request.is_ajax():
        params = request.GET
        # 获取查询参数
        PAGE_SIZE = 10
        page_no = params.get('pageNo', 1)
        query_str = params.get('q', '')
        queries = [Q(comment__contains=q) for q in query_str.split('+') if q]

        # 获取查询结果，并处理为json可以输出格式
        data = {}
        all_comments = product.comments_set.filter(
            pid=pid,
            *queries,
        ).order_by('-pub_date')
        if all_comments.exists():
            # 计算分页
            c_paginator = Paginator(all_comments, PAGE_SIZE)
            try:
                comments = c_paginator.page(page_no)
            except PageNotAnInteger:
                page_no = 1
                comments = c_paginator.page(page_no)
            except EmptyPage:
                comments = c_paginator.page(c_paginator.num_pages)
            finally:
                html = render_to_string(
                    'comments.html',
                    context={
                        'comments': comments,
                        'page_no': int(page_no),
                        'page_size': PAGE_SIZE,
                        'q': query_str,
                        'c_paginator': c_paginator,
                        'pid': pid,
                    }
                )
                data['page'] = html
                data['status'] = 200
        else:
            data['status'] = 404
            data['error'] = '未查询到相关内容！'
        return JsonResponse(data, status=data['status'])

    return render(
        request,
        'detail.html',
        locals()
    )


@require_http_methods(['GET'])
def sentiment(request, pid):
    try:
        product = Products.objects.get(pid=pid)
    except Products.DoesNotExist as _:
        return render(
            request,
            '404.html',
            status=404
        )
    return render(
        request,
        # 'detail.html',
        'sentiment.html',
        locals()
    )


# 分析页面数据获取/ajax
@require_http_methods(['GET'])
def analysis(request, pid):
    product = get_object_or_404(Products, pid=pid)
    if request.is_ajax():
        # params = request.GET
        # # 获取查询参数
        # query_str = params.get('q', '')
        # queries = [Q(comment__contains=q) for q in query_str.split('+') if q]

        
        comments = product.comments_set.filter(
            pid=pid,
            # *queries,
        )
        # 记录查询结果，输出为json
        data = {}

        # if comments.exists():
        # 基于获取到的评论内容计算舆情分析
        # 评论数量
        c_count = comments.count()
        # 平均情感倾向
        sent_avg = f"{comments.aggregate(Avg('sentiments'))['sentiments__avg']:0.2f}"
        # 正向数量
        plus = comments.filter(sentiments__gte=0.5).count()
        # 负面数量
        minus = c_count - plus

        # card block需要的数据
        data['card_params'] = {
            'c_count': c_count,
            'plus': plus,
            'minus': minus,
            'sent_avg': sent_avg,
        }
        # data['pie_page'] = render_to_string(
        #     'pie.html',
        #     locals(),
        # )

        # table 需要的数据
        data['table_data'] = list(comments.values(
            "cid",
            "username",
            "pub_date",
            "comment",
            "sentiments",
        ))
        data['pie_page'] = None
        data['status'] = 200

        # 设置自定义的JSONEncoder用于日期的格式显示
        # 标准JSONEncoder的日期格式化字符串显示不美观
        return JsonResponse(
            data,
            status=data['status'],
            safe=False,
            encoder=DatetimeJSONEncoder
            )

    return render(
        request,
        'sentiment.html',
        locals()
    )