
from django.urls import path, include
from .views import (PostList, PostSearch, PostDetail, PostCreate,
                    PostUpdate, PostDelete, subscriptions, CategoryListView, subscribe, upgrade_user)
from . import views

urlpatterns = [

    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
    # path('categories/<int:pk>/subscribe', subscriptions, name='subscriptions'),

    # path('<int:post_id>/share/', views.post_share, name='post_share'),
]
