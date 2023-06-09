from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('news/', include('news.urls')),
]

