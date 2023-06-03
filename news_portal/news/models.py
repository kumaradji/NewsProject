from audioop import reverse

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


# Модель, содержащая объекты всех авторов
# имеет следующие поля:
class Author(models.Model):
    # связь «один к одному» с встроенной моделью пользователей User;
    # когда имеем отношение ко встроенной модели, ее нужно импортировать
    # from django.contrib.auth.models import User
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    # рейтинг пользователя
    ratingAuthor = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    # метод обновления рейтинга пользователя,
    # суммарный рейтинг пользователя за его посты, лайки и прочее
    def update_rating(self):
        # вместо цикла for можно реализовать сбор данных таким образом
        # aggregate, происходит сбор всех данных определенного поля данного пользователя
        # мы суммируем поле 'rating' класс Post
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        # для комментов суммирование рейтинга, мы суммируем поле 'rating' класс Comment
        # так как "commentPost = models.ForeignKey", в связь добавится "authorUser"
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        # складываем две переменные, рейтинг за статью (посты), и рейтинг за комменты
        self.ratingAuthor = pRat * 3 + cRat
        # сохранение модели в БД
        self.save()

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.authorUser}'


# Категории новостей/статей — темы, которые они отражают (спорт, политика,образование и т. д.).
class Category(models.Model):
    # Имеет единственное поле: название категории. Поле должно быть уникальным
    # (в определении поля необходимо написать параметр unique = True).
    # Максимальную длину строки берут в н-ой степени, 2,4,8,16,32...128,256
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', through='Subscriber')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('news_category', kwargs={'category_id': self.id})


# Статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
class Post(models.Model):
    # поле с выбором — «статья» или «новость»
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    # связь «один ко многим» с моделью Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)

    # автоматически добавляемая дата и время создания
    date = models.DateTimeField(auto_now_add=True)

    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)
    category = models.ManyToManyField(Category, through='PostCategory')

    # заголовок статьи/новости
    title = models.CharField(max_length=255)

    # текст статьи/новости
    text = models.TextField()

    # рейтинг статьи/новости
    # в данное поле мы сохраняем значение рейтинга, добавляя либо +1(лайк), либо -1 (дизлайк)
    # через методы def like(self) и def dislike(self)
    rating = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    # превью статьи, мы взяли часть статьи (первые 120 символа) и прибавили многоточие в конце
    def preview(self):
        return self.text[0:120] + '...'

    # метод описания лайков
    def like(self):
        self.rating += 1
        self.save()

    # метод описания дизлайков
    def dislike(self):
        self.rating -= 1
        self.save()

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.title}: {self.author}'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостями
    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

    def __str__(self):
        return f'{self.post.title} ({self.category.name})'


# Под каждой новостью/статьей можно оставлять комментарии,
# поэтому необходимо организовать их способ хранения
class Comment(models.Model):
    # связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # связь «один ко многим» с встроенной моделью User
    # (комментарии может оставить любой пользователь, не только автор)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # текст комментария
    text = models.TextField()

    # дата и время создания комментария
    created = models.DateTimeField(auto_now_add=True)

    # рейтинг комментария
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    # метод описания лайков
    def like(self):
        self.rating += 1
        self.save()

    # метод описания дизлайков
    def dislike(self):
        self.rating -= 1
        self.save()

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.user.username} про "{self.post}"'


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f'{self.user.username} подписан на {self.category}'
