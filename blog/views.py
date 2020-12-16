from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import *
from .forms import *
from .utils import *

from django.contrib.auth.mixins import LoginRequiredMixin


def posts_list(request):
    title = 'Записки склерозника'
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts, 'title': title})


class PostDetail(ObjectDetailMixin, View):

    model = Post
    template = 'blog/post_list.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'post_list_url'
    raise_exception = True
