from django.shortcuts import (
    # render,
    redirect,
    # get_object_or_404,
)
from django.urls import reverse



def home(request):
    return redirect(f'{reverse("movies:index")}')
