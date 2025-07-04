"""
URL configuration for edutrack_projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# edutrack_projeto/urls.py
from django.contrib import admin
from django.urls import path
from edutrack import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('boletim/', views.Boletim, name='boletim_escolar'),
    path('participacao/<int:pk>/', views.participacao, name='participacao'),
    path('formsAlunos/', views.aluno_create, name='forms_aluno'),
    path('alunoLista/', views.aluno_list, name='aluno_lista'),
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('professor/', views.professor, name='professor'),
    path('', views.professor, name='home'),
    path('painel-turmas/', views.painel_turmas, name='painel_turmas'),
    path('resumo/', views.resumo, name='resumo'),
    # rotas para “Turma”
    path('turmas/<int:turma_id>/presenca/', views.turma_presenca, name='turma_presenca'),
    path('turmas/<int:turma_id>/tarefas/', views.turma_tarefas, name='turma_tarefas'),
    path('turmas/<int:turma_id>/diario/',    views.turma_diario,   name='turma_diario'),
]

