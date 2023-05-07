from django.utils import timezone

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category
from news_portal import settings


# рассылка подписчикам списка публикаций за неделю
# через celery.py/app.conf.beat_schedule
@shared_task
def send_email():
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# рассылка подписчикам уведомления о новой публикаций
@shared_task
def new_post_notify(instance_id):
    instance = Post.objects.get(pk=instance_id)
    categories = instance.category.all()
    subscribers: list[str] = []

    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]

    for mail in subscribers:
        html_context = render_to_string(
            'post_created_email.html',
            {
                'text': instance.preview,
                'link': f'{settings.SITE_URL}/news/{instance_id}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=instance.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )

        msg.attach_alternative(html_context, 'text/html')
        msg.send()
