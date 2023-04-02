from django.views.generic import ListView, DetailView

from .models import *


class PostList(ListView):
    model = Post
    template_name = 'news_portal_page.html'
    context_object_name = 'news'

    # def get_queryset(self):
    #     return Post.objects.all()


class PostDetail(DetailView):
    model = Post
    template_name = 'post_list.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
