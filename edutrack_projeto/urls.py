# edutrack_projeto/urls.py (VERSÃO FINAL E CORRIGIDA)

from django.contrib import admin
from django.urls import path, include
from edutrack import views

# --- Imports adicionais para servir arquivos estáticos em desenvolvimento ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Suas rotas existentes
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('boletim/', views.Boletim, name='boletim_escolar'),
    path("participacao/<int:pk>/", views.participacao, name="participacao"), 
    path('formsAlunos/', views.aluno_create, name='forms_aluno'),
    path('alunoLista/', views.aluno_list, name='aluno_lista'),  
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('tarefas/', views.tarefas_home, name='tarefas'),
    path('desempenho/<int:aluno_pk>/', views.desempenho_geral_view, name='desempenho_aluno'),
    path('turmas-overview/', views.turmas_overview_view, name='turmas_overview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)