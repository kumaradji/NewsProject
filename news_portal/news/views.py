from django.views.generic import ListView, DetailView

from .models import *


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'



class PostDetail(DetailView):
    model = Post
    template_name = 'post_view.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
