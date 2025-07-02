# edutrack/admin.py

from django.contrib import admin
from .models import * 


admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Nota)
admin.site.register(Responsavel)
admin.site.register(Atividade)
admin.site.register(Education)
admin.site.register(Turma)
admin.site.register(Calendario)
admin.site.register(Resumo)
admin.site.register(ConteudoDia)
admin.site.register(Quiz)
admin.site.register(Relatorio)
admin.site.register(GradeHorario)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turma', 'user')
    search_fields = ('nome', 'matricula', 'turma')
