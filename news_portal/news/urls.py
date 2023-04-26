from django.urls import path, include
from .views import (PostList, PostSearch, PostDetail, PostCreate,
                    PostUpdate, PostDelete, subscriptions, upgrade_user)
from . import views


class CategoruListView:
    pass


urlpatterns = [

    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('categories/<int:pk>/', CategoruListView.as_view(), name='category_list'),
]
