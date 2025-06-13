from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome', 'matricula', 'turma',
            'pontualidade', 'participacao_aula', 'entregas_tarefas',
            'comportamento_funcionarios', 'participacao_oficinas',
            'comportamento_sala', 'participacao_plataformas'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'matricula': forms.TextInput(attrs={'placeholder': 'Ex: 2025.1'}),
            'turma': forms.TextInput(attrs={'placeholder': 'Turma / Curso'}),
            # campos numéricos
            'pontualidade': forms.NumberInput(attrs={'min':0, 'max':100}),
            'participacao_aula': forms.NumberInput(attrs={'min':0, 'max':100}),
            'entregas_tarefas': forms.NumberInput(attrs={'min':0, 'max':100}),
            'comportamento_funcionarios': forms.NumberInput(attrs={'min':0, 'max':100}),
            'participacao_oficinas': forms.NumberInput(attrs={'min':0, 'max':100}),
            'comportamento_sala': forms.NumberInput(attrs={'min':0, 'max':100}),
            'participacao_plataformas': forms.NumberInput(attrs={'min':0, 'max':100}),
        }
        labels = {
            'pontualidade': 'Pontualidade (%)',
            'participacao_aula': 'Participação em aula (%)',
            'entregas_tarefas': 'Entregas de tarefas (%)',
            'comportamento_funcionarios': 'Comportamento c/ funcionários (%)',
            'participacao_oficinas': 'Participação em oficinas (%)',
            'comportamento_sala': 'Comportamento em sala (%)',
            'participacao_plataformas': 'Participação em plataformas (%)',
        }
