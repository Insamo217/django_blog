from django.db import models
from datetime import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField('Заголовок поста', max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    text = models.TextField('Текст поста', blank=True, db_index=True)
    date_pub = models.DateTimeField('Дата публикации', default=datetime.now())

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey\
        (User, related_name='users', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    text = models.TextField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name='Видимость комментарии', default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Комментарий к {}'.format(self.post)