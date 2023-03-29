from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'postlist.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = "Следите за новостями!"
        return context


# class CommentDetail(DetailView):
#     model = Comment
#     template_name = 'news.html'
#     context_object_name = 'post'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# class AuthorDetail(DetailView):
#     model = Author
#     template_name = 'news.html'
#     context_object_name = 'post'
