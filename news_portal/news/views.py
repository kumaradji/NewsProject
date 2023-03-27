# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'database/news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    template_name = 'database/post.html'
    context_object_name = 'post'


