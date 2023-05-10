from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_managers, mail_admins

from news_portal import settings


def add_to_common_group(user):
    group = Group.objects.get(name='common')
    group.user_set.add(user)


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        # mail_managers(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь {user.username} зарегистрировался на сайте.'
        # )

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user
