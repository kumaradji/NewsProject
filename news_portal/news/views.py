from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Следите за новостями!"
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

