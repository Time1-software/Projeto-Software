# edutrack_projeto/urls.py (VERSÃO FINAL E CORRIGIDA)

from django.contrib import admin
from django.urls import path, include
from edutrack import views

# --- Imports adicionais para servir arquivos estáticos em desenvolvimento ---
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from edutrack import views
from django.views.generic import RedirectView
from edutrack.views import (
    CustomLoginView,
    CustomLogoutView,
    SignupView,
    SignupSuccessView,
    BemvindoAlunoView,
    BemvindoProfessorView,
    BemvindoPaiView,
    BemvindoAdmView,
)


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
    path('gradeAluno/', views.grade_aluno, name='grade_aluno'),
    path('painelAluno/', views.painel_aluno, name='painelAluno') ,
    path('dashboard-pais/', views.desempenho_geral_view, name='dashboard_pais'),

    #LOGIN
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    
    path('login/',  CustomLoginView.as_view(),  name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('signup/',         SignupView.as_view(),        name='signup'),
    path('signup/success/', SignupSuccessView.as_view(), name='signup-success'),

    path('bemvindo/aluno/',     BemvindoAlunoView.as_view(),     name='bem_vindo_aluno'),
    path('bemvindo/professor/', BemvindoProfessorView.as_view(), name='bem_vindo_professor'),
    path('bemvindo/pai/',       BemvindoPaiView.as_view(),       name='bem_vindo_pai'),
    path('bemvindo/adm/',       BemvindoAdmView.as_view(),       name='bem_vindo_adm'),

    path('painelAluno/', views.painel_aluno, name='painelAluno') ,
    path('calendario/', views.calendario_view, name='calendario'),
    path('criar-tarefa/', views.criar_tarefa, name='criar_tarefa'), 
    path('turmas-overview/', views.turmas_overview_view, name='turmas_overview'),

    #Area Usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('vincular-responsavel/', views.vincular_responsavel, name='vincular_responsavel'),
    path('editar_aluno_responsavel_inline/', views.editar_aluno_por_responsavel, name='editar_aluno_responsavel_inline'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)