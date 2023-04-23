from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .views import PostCreate


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='newuser')
        instance.groups.add(group)
    else:
        return


# проверить работу
# @receiver(post_save, sender=Post)
# def notify_about_new_post(sender, instance, send_notifications=None, **kwargs):
# if kwargs['action'] == 'post_add':
#     postcategory = instance.postCategory.all()
#     subscribers: list[str] = []
#     for category in postcategory:
#         subscribers += category.subscribers.all()
#
#     subscribers_email = [s.email for s in subscribers]
#     send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribers_email)

@receiver(post_save, sender=PostCreate)
def news_created(instance, created, **kwargs):
    if not created:
        return
    emails = User.objects.filter(
        subscriptions__category=instance.id).values_list('email', flat=True)
    subject = f'Новая публикация в категории {instance.postCategory}'

    text_content = (
        f'Публикация: {instance.author}\n'
        f'Тема: {instance.text}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Публикация: {instance.author}<br>'
        f'Тема: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на публикацию</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
