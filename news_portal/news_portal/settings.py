import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-7&7zcad^v^)+=!p-tfekn9i79a!6!60(l9ss1aoxu5(ke&)(av'
DEBUG = True
ALLOWED_HOSTS = []

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# mandatory — не пускать пользователя на сайт до момента подтверждения почты
# optional — сообщение о подтверждении почты будет отправлено,
# но пользователь может залогиниться на сайте без подтверждения почты
ACCOUNT_EMAIL_VERIFICATION = 'optional'
# Указали форму для дополнительной обработки регистрации пользователя
# ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}
# позволит избежать дополнительного входа
# и активирует аккаунт сразу, как только мы перейдём по ссылке
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# хранит количество дней, когда доступна ссылка на подтверждение регистрации
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 10
# Настройки почты отправляется на консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Настройки почты отправляется на реальный почтовый ящик
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "kumaradji@yandex.ru"
EMAIL_HOST_PASSWORD = "tltiblvgbecfzhds"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_SUBJECT_PREFIX = 'NewsPortal_Kumar'

DEFAULT_FROM_EMAIL = "kumaradji@yandex.ru"
SERVER_EMAIL = "kumaradji@yandex.ru"
ADMINS = (
    ('Кумар', 'kumaradji@me.com'),
)
MANAGERS = (
    ('Кумар', 'kumaradji@gmail.com'),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'django_apscheduler',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'news',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'news_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'news_portal.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_REDIRECT_URL = "/news"
