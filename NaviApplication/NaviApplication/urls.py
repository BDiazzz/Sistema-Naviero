
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import login_general
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('recursos/', include('GestorRecursos.urls')),
    path('navios/', include('GestorNavios.urls')),
    path('login/', login_general, name='login_general'),

    path('',lambda request: redirect('login_general'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
