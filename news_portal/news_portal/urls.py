
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # # Делаем так, чтобы все адреса из нашего приложения (news_portal/urls.py)
    # # подключались к главному приложению с префиксом news/.
    path('news/', include('news.urls')),
    path('post/', include('django.contrib.flatpages.urls')),
]
