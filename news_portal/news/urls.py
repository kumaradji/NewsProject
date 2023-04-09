from django.urls import path, include
from .views import *

urlpatterns = [

    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='post_search'),

    path('create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', PostCreate.as_view(), name='post_create'),

    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),

    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
