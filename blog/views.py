from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .utils import *

from django.contrib.auth.mixins import LoginRequiredMixin


def posts_list(request):
    title = 'Записки склерозника'
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html',
                  context={'posts': posts, 'title': title})


def user_login(request):
    title = 'Авторизация'
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list_url'))
                else:
                    return HttpResponse('User not active')
            else:
                messages.error(request, 'Данные введены неверно!')

    else:
        form = UserLoginForm()

    context = {
        'form': form, 'title': title
    }

    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('post_list_url')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('user_login')

    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'blog/register.html', context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


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
