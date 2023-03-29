from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'news.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = "Следите за новостями!"
        return context

    # def news_page(self):
    #     all_news = Post.objects.all()
    #     print(all_news)

#
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
