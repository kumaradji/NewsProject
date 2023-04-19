from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Exists
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from .filters import PostFilter
from .forms import PostForm
from .models import *
from django.urls import reverse_lazy, reverse


class PostList(ListView):
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


class PostSearch(ListView):
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


class PostDetail(DetailView):
    model = Post
    template_name = 'post_view.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


# Представление для создания новости
class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.create_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.is_news = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


# Представление для изменения новости
class PostUpdate(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.post_edit',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


# Представление удаляющее новость
class PostDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('news.post_delete',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
