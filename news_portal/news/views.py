from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PostFilter
from django_filters import FilterSet, DateTimeFilter
from .forms import PostForm
from django.forms import DateTimeInput
from .models import *
from django.urls import reverse_lazy


class PostList(LoginRequiredMixin, ListView):
    model = Post
    # указываем способ сортировки
    ordering = '-dateCreation'
    # указываем шаблон представления
    template_name = 'news.html'
    # указываем переменную, которую будем использовать в
    # шаблоне news.html
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostSearch(LoginRequiredMixin, ListView):
    raise_exception = True
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search_page.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search_page'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['cat_selected'] = 0
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_view.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(postCategory__slag=self.kwargs['news'])


class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author = self.request.user.author
        post.quantity = 13
        return super().form_valid(form)


class NewsCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        # post.isnews = True
        return super().form_valid(form)


# Добавляем представление для изменения товара.
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
