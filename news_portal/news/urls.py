from django.urls import path
from .views import (PostList, PostSearch, PostDetail, PostCreate,
                    PostUpdate, PostDelete, subscriptions,
                    CategoryListView, subscribe, upgrade_user, Index)
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post'),

    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('index/', Index.as_view(), name='index'),

]
