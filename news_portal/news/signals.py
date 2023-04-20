from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='newuser')
        instance.groups.add(group)


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Новая публикация в категории {instance.category}'

    text_content = (
        f'Публикация: {instance.title}\n'
        f'Тема: {instance.text}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Публикация: {instance.title}<br>'
        f'Тема: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на публикацию</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
