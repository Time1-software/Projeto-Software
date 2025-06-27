from django.contrib import admin
from .models import * 
from .models import Aluno

# Register your models here.

admin.site.register(Education)
admin.site.register(Nota)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turma')
    search_fields = ('nome', 'matricula', 'turma')

admin.site.register(Turma)
admin.site.register(Professor)
admin.site.register(Atividade)
admin.site.register(Calendario)
admin.site.register(Resumo)
admin.site.register(ConteudoDia)
admin.site.register(Quiz)
admin.site.register(Relatorio)
admin.site.register(Chat)
admin.site.register(GradeHorario)