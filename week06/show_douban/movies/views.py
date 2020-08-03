from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

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
    comments = movie.comments_set.all()
    return render(
        request,
        'detail.html',
        locals()
    )


# def comments(request, mk):
#     pass
