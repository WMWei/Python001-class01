from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string

from .models import Comments, Movies


def index(request):
    params = request.GET
    start = int(params.get('start', 0))
    pagesize = int(params.get('pagesize', 8))
    if start % pagesize != 0:
        start = 0
    movies = Movies.objects.order_by('-rate')[start:start + pagesize]
    movies_count = Movies.objects.count()
    cur_page_num = start // pagesize + 1
    # if movies_count % pagesize == 0:
    #     end_page_num = movies_count // pagesize
    # else:
    #     end_page_num = movies_count // pagesize + 1
    return render(
        request,
        'index.html',
        locals(),
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
        start = int(params.get('start', 0))
        pagesize = int(params.get('pagesize', 10))
        q_str = params.get('q', '')
        queries = [Q(comment__contains=q) for q in q_str.split('+') if q]

        # 获取查询结果，并处理为json可以输出格式
        data = {}
        all_comments = movie.comments_set.filter(
            movie_id=mk,
            rate__gte=8,
            *queries,
        ).order_by('-date')
        comments_count = all_comments.count()
        comments = all_comments[start:start + pagesize]
        if comments.exists():
            html = render_to_string(
                'comments.html',
                context={
                    'comments': comments,
                    'start': start,
                    'pagesize': pagesize,
                    'q': q_str,
                    'comments_count': comments_count,
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
