from django.contrib import admin
from django.urls import path
from participacao.views import aluno_list, aluno_create, participacao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', aluno_list, name='aluno_list'),
    path('aluno/novo/', aluno_create, name='aluno_create'),
    path('aluno/<int:pk>/', participacao, name='participacao'),
]
