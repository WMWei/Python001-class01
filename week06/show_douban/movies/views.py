from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from .models import Comments, Movies


def index(request):
    params = request.GET
    page_no = int(params.get('pageNo', 1) or 1)
    page_size = int(params.get('pageSize', 4) or 4)
    movies = Movies.objects.all().order_by('-rate')
    paginator = Paginator(movies, page_size)
    try:
        movies = paginator.page(page_no)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    return render(
        request,
        'index.html',
        context={
            'page_no': page_no,
            'page_size': page_size,
            'paginator': paginator,
            'movies': movies,
        },
    )


def detail(request, mk):
    movie = get_object_or_404(Movies, movie_id=mk)
    # comments = movie.comments_set.filter(rate__gte=8)
    return render(
        request,
        'detail.html',
        locals()
    )


def comments(request, mk):
    movie = get_object_or_404(Movies, movie_id=mk)
    if request.is_ajax() and request.method == "GET":
        params = request.GET

        # 获取查询参数
        page_no = int(params.get('pageNo', 1) or 1)
        page_size = int(params.get('pageSize', 10) or 10)
        q_str = params.get('q', '')
        queries = [Q(comment__contains=q) for q in q_str.split('+') if q]

        # 获取查询结果，并处理为json可以输出格式
        data = {}
        all_comments = movie.comments_set.filter(
            movie_id=mk,
            rate__gte=8,
            *queries,
        ).order_by('-date')
        if all_comments.exists():
            c_paginator = Paginator(all_comments, page_size)
            try:
                comments = c_paginator.page(page_no)
            except PageNotAnInteger:
                comments = c_paginator.page(1)
            except EmptyPage:
                comments = c_paginator.page(c_paginator.num_pages)
            finally:
                html = render_to_string(
                    'comments.html',
                    context={
                        'comments': comments,
                        'page_no': page_no,
                        'page_size': page_size,
                        'q': q_str,
                        'c_paginator': c_paginator,
                        'movie_id': mk,
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
