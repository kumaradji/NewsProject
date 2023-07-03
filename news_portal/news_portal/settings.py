import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-7&7zcad^v^)+=!p-tfekn9i79a!6!60(l9ss1aoxu5(ke&)(av'
DEBUG = True
ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = "/news"
LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# CACHES = {
#     'default': {
#         'TIMEOUT': 30,
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
#     }
# }

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# mandatory — не пускать пользователя на сайт до момента подтверждения почты
# optional — сообщение о подтверждении почты будет отправлено,
# но пользователь может залогиниться на сайте без подтверждения почты
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Указали форму для дополнительной обработки регистрации пользователя
# позволит избежать дополнительного входа
# и активирует аккаунт сразу, как только мы перейдём по ссылке
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# хранит количество дней, когда доступна ссылка на подтверждение регистрации
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 10
# Настройки почты отправляется на консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Настройки почты отправляется на реальный почтовый ящик
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# хост почтового сервера
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
# логин почтового сервера
EMAIL_HOST_USER = 'Ku79313081435'
# пароль пользователя почтового сервера
# EMAIL_HOST_PASSWORD = "mcoiviutbawsxidk"
EMAIL_HOST_PASSWORD = os.getenv('DEFAULT_FROM_EMAIL')
DEFAULT_FROM_EMAIL = 'Ku79313081435@yandex.ru'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

SERVER_EMAIL = "Ku79313081435@yandex.ru"
EMAIL_SUBJECT_PREFIX = 'NewsPortal_kumaradji'

ADMINS = (
    ('Кумар', 'kumaradji@me.com'),
)
MANAGERS = (
    ('Кумар', 'kumaradji@gmail.com'),
)

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.humanize',
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
    'news.apps.NewsConfig',

]

SITE_ID = 1
SITE_URL = 'http://127.0.0.1:8000'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'news.middlewares.TimezoneMiddleware',

    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standart': {
            'format': '{asctime} :: {levelname} -- {message}',
            'style': '{',
        },
        'forinfo': {
            'format': '{asctime} :: {levelname} -- {module} : {message}',
            'style': '{',
        },
        'forwarning': {
            'format': '{asctime} :: {levelname} -- {pathname} : {message}',
            'style': '{',
        },
        'forerror': {
            'format': '{asctime} :: {levelname} -- {pathname} / {exc_info} :{message}',
            'style': '{',
        },
        'security': {
            'format': '{asctime} :: {levelname} -- {module} : {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        # В файл general.log должны выводиться сообщения уровня INFO и выше только с
        # указанием времени, уровня логирования, модуля, в котором возникло
        # сообщение (аргумент module) и само сообщение. Сюда также попадают сообщения с регистратора django.
        'general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_false'],
            'filename': 'general.log',
            'formatter': 'forinfo'
        },
        # В файл errors.log должны выводиться сообщения только уровня ERROR и CRITICAL.
        # В сообщении указывается время, уровень логирования, само сообщение,
        # путь к источнику сообщения и стэк ошибки. В этот файл должны попадать
        # сообщения только из логгеров django.request, django.server, django.template, django.db.backends.
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'forerror'
        },
        # В консоль должны выводиться все сообщения уровня DEBUG и выше,
        # включающие время, уровень сообщения, сообщения.
        'console_standart': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standart',
        },
        # Для сообщений WARNING и выше дополнительно должен
        # выводиться путь к источнику события (используется аргумент pathname в форматировании).
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'forwarning',
        },
        # А для сообщений ERROR и CRITICAL еще должен выводить стэк ошибки (аргумент exc_info).
        # Сюда должны попадать все сообщения с основного логгера django.
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'forerror',
        },
        # На почту должны отправляться сообщения уровней ERROR и выше из django.request
        # и django.server по формату, как в errors.log, но без стэка ошибок.
        # Более того, при помощи фильтров нужно указать, что в консоль сообщения отправляются
        # только при DEBUG = True
        'console_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'forwarning',
        },
        # а на почту только при DEBUG = False.
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'forwarning',
        },
        # в файл general.log — только при DEBUG = False.
        'admins_general_file': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'forwarning',
        },
        # В файл security.log должны попадать только сообщения, связанные с безопасностью,
        # а значит только из логгера django.security. Формат вывода предполагает время,
        # уровень логирования, модуль и сообщение
        'security': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'security',
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console_standart',
        #                  'console_warning',
        #                  'console_error',
        #                  'general',
        #                  'errors',
        #                  'security',
        #                  'console_admins',
        #                  'mail_admins',
        #                  'admins_general_file'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        'django.request': {
            'handlers': ['errors',
                         'mail_admins',
                         'general',
                         'admins_general_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['errors',
                         'mail_admins',
                         'admins_general_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.*': {
            'handlers': ['security'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

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
# USE_L10N = True
LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]