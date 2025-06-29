# edutrack/admin.py

from django.contrib import admin
from .models import * 


admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Nota)
admin.site.register(Responsavel)
admin.site.register(Atividade)
admin.site.register(Education)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turma')
    search_fields = ('nome', 'matricula', 'turma')
