from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import OuterRef, Exists
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .filters import PostFilter
from .forms import PostForm, EmailPostForm
from .models import *
from django.urls import reverse_lazy, reverse


class PostList(LoginRequiredMixin, ListView):
    model = Post
    # указываем способ сортировки
    ordering = '-dateCreation'
    # указываем шаблон представления
    template_name = 'news.html'
    # указываем переменную, которую будем использовать в
    # шаблоне news.html
    context_object_name = 'news'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    # список статей конкретной категории
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-dateCreation')
        return queryset

    # создаём кнопку подписаться, если ещё не подписан
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


# реализует подписаться или отписаться от категории
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = "Вы успешно подписались на рассылку новостей категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class PostSearch(LoginRequiredMixin, ListView):
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
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_view.html'
    raise_exception = True
    context_object_name = 'post'


# Представление для создания новости
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.is_news = True
        post.author = self.request.user.author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


# Представление для изменения новости
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.post_edit',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


# Представление удаляющее новость
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('news.post_delete',)
    queryset = Post.objects.all()
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


# при добавлении нового пользователя в группу авторы или в newuser
@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)

    group = Group.objects.get(name='newuser')
    if not user.groups.filter(name='newuser').exists():
        group.user_set.add(user)

    Author.objects.create(authorUser=User.objects.get(pk=user.id))

    return redirect('/')
