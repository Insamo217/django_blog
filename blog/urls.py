from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', posts_list, name='post_list_url'),
    path('create/', PostCreate.as_view(), name='post_create_url'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('post/<str:slug>/', post_detail, name='post_detail_url'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', register, name='register'),
    path('like/', like_post, name='like_post'),
    path('about_ms/', about_ms, name='about_ms')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)