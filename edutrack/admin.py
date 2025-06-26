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