from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from news_portal import settings
from .models import PostCategory, Subscriber
from .views import PostCreate
from news.tasks import new_post_notify


# рассылка подписчикам при создании публикации
def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


# рассылка подписчикам при создании публикации через tasks.py
@receiver(m2m_changed, sender=PostCategory)
def new_post_notification(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_notify.delay(instance.id)

# рассылка подписчикам при создании публикации (без celery)
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     # только если статья создалась
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         # список подписчиков на категорию модели User
#         subscribers: list[str] = []
#         for category in categories:
#             # добавляем в список подписчиков категории
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


# создаём рассылку по почте когда создается новая публикация
# @receiver(post_save, sender=PostCreate)
# def news_created(instance, created, **kwargs):
#     if not created:
#         return
#     emails = User.objects.filter(
#         subscriptions__category=instance.id).values_list('email', flat=True)
#     subject = f'Новая публикация в категории {instance.category}'
#
#     text_content = (
#         f'Публикация: {instance.author}\n'
#         f'Тема: {instance.text}\n\n'
#         f'Ссылка на публикацию: http://127.0.0.1{instance.get_success_url()}'
#     )
#     html_content = (
#         f'Публикация: {instance.author}<br>'
#         f'Тема: {instance.text}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_success_url()}">'
#         f'Ссылка на публикацию</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
