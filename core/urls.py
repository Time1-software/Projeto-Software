from django.contrib import admin
from django.urls import path
from participacao.views import aluno_list, aluno_create, participacao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', aluno_list, name='aluno_list'),
    path('aluno/novo/', aluno_create, name='aluno_create'),
    path('aluno/<int:pk>/', participacao, name='participacao'),
    path("professor/", views.professor, name="professor"),
    path("painel-turmas/", views.painel_turmas, name="painel_turmas"),
    path("resumo/", views.resumo, name="resumo"),
    path('turmas/<int:turma_id>/presenca/', views.turma_presenca, name='turma_presenca'),
    path('turmas/<int:turma_id>/tarefas/',   views.turma_tarefas,   name='turma_tarefas'),
]
