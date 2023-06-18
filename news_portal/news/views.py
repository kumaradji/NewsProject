from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import OuterRef, Exists
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .filters import PostFilter
from .forms import PostForm
from .models import *
from django.urls import reverse_lazy, reverse
from django.core.cache import cache  # импортируем наш кэш


def language_selection(request):
    if request.method == 'POST':
        language_code = request.POST.get('language')
        next_url = request.POST.get('next', '/')
        response = HttpResponseRedirect(next_url)
        response.set_cookie('django_language', language_code)
        return response

    redirect_to = request.GET.get('next', '/')
    current_language_code = request.LANGUAGE_CODE

    context = {
        'redirect_to': redirect_to,
        'current_language_code': current_language_code,
    }

    return render(request, 'language_selection.html', context)


def set_timezone(request):
    if request.method == 'POST':
        # Получаем выбранный часовой пояс из POST-запроса
        timezone_name = request.POST.get('timezone')
        # Устанавливаем новый часовой пояс в сессию пользователя
        request.session['django_timezone'] = timezone_name
    # Редиректим пользователя на главную страницу
    return redirect('/news')


def home(request):
    # Получаем текущий часовой пояс из сессии пользователя
    current_timezone = request.session.get('django_timezone', 'UTC')
    # Получаем текущую дату и время в выбранном часовом поясе
    current_datetime = timezone.now().astimezone(timezone.get_timezone(current_timezone))
    # Передаем текущую дату и время в контекст шаблона
    context = {'current_datetime': current_datetime}
    return render(request, 'news.html', context)


# Представление для главной страницы
class PostList(LoginRequiredMixin, ListView):
    model = Post
    # указываем способ сортировки
    ordering = '-date'
    # указываем шаблон представления
    template_name = 'news.html'
    # указываем переменную, которую будем использовать в шаблоне news.html
    context_object_name = 'news'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    ordering = '-date'
    paginate_by = 3

    # список статей конкретной категории
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    # создаём кнопку подписаться, если ещё не подписан
    def get_context_data(self, **kwargs):
        # общаемся к содержимому контекста нашего представления
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        # context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['category'] = self.category
        return context


# Представление для поиска статей
class PostSearch(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date'
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


# Представление для получения деталей о посте
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_view.html'
    raise_exception = True
    context_object_name = 'post'

    queryset = Post.objects.all()

    # переопределяем метод получения объекта, как ни странно
    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'post-{self.kwargs["pk"]}',
    #                     None)
    #
    #     # если объекта нет в кэше, то получаем его и записываем в кэш
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #
    #     return obj
    #


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


# при добавлении нового пользователя в группу авторы
@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)

    Author.objects.create(authorUser=User.objects.get(pk=user.id))

    return redirect('/')


# реализует страницу подписки на категорию
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = "Вы успешно подписались на рассылку новостей категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
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
