from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from news_portal import settings
from .models import PostCategory
from .views import PostCreate


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


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

    # @receiver(post_save, sender=User)
    # def add_user_to_group(sender, instance, created, **kwargs):
    #     if created:
    #         group = Group.objects.get(name='newuser')
    #         instance.groups.add(group)
    #     else:
    #         return
    #
    #
    # @receiver(post_save, sender=PostCreate)
    # def news_created(instance, created, **kwargs):
    #     if not created:
    #         return
    #     emails = User.objects.filter(
    #         subscriptions__category=instance.id).values_list('email', flat=True)
    #     subject = f'Новая публикация в категории {instance.postCategory}'
    #
    #     text_content = (
    #         f'Публикация: {instance.author}\n'
    #         f'Тема: {instance.text}\n\n'
    #         f'Ссылка на публикацию: http://127.0.0.1{instance.get_absolute_url()}'
    #     )
    #     html_content = (
    #         f'Публикация: {instance.author}<br>'
    #         f'Тема: {instance.text}<br><br>'
    #         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
    #         f'Ссылка на публикацию</a>'
    #     )
    #     for email in emails:
    #         msg = EmailMultiAlternatives(subject, text_content, None, [email])
    #         msg.attach_alternative(html_content, "text/html")
    #         msg.send()
