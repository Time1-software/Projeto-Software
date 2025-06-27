"""
URL configuration for hello_world project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from hello_world.core import views as core_views
from edutrack import views as edutrack_views

urlpatterns = [
    # Página inicial do projeto (core app)
    path("", core_views.index, name="home"),

    # Admin do Django
    path("admin/", admin.site.urls),

    # Página Bem-Vindo Professor (app edutrack)
    path("professor/", edutrack_views.professor, name="professor"),
    path("painel-turmas/", edutrack_views.painel_turmas, name="painel_turmas"),
    path("resumo/", edutrack_views.resumo, name="resumo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()