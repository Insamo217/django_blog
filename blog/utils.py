from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import View
from .models import *


class ObjectDetailMixin:
    title = None
    model = None
    template = None
    comments = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        comments = Comment.objects.filter(post=obj).order_by('-id')
        title = self.model
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj, 'title': title,
                               'comments': comments})


class ObjectCreateMixin:
    title = None
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        title = 'Создание поста'
        return render(request, self.template,
                      context={'form': form, 'title': title})

    def post(self, request):
        bound_form = self.model_form(request.POST)
        title = 'Создание поста'
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template,
                      context={'form': bound_form, 'title': title})


class ObjectUpdateMixin():
    title = None
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        title = 'Редактирование поста'
        return render(request, self.template,
                      context={'form': bound_form,
                               self.model.__name__.lower(): obj,
                               'title': title})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        title = 'Редактирование поста'

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template,
                      context={'form': bound_form,
                               self.model.__name__.lower(): obj,
                               'title': title})


class ObjectDeleteMixin:
    title = None
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        title = 'Удаление поста'
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj,
                               'title': title})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        title = 'Удаление поста'
        return redirect(reverse(self.redirect_url), context={'title': title})
