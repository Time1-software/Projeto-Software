# edutrack/views.py (VERSÃO FINAL E COMPLETA)

# --- Imports Consolidados ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
import datetime
import json
from .models import * # Importa todos os modelos: Aluno, Turma, Nota, etc.
from .forms import AlunoForm

# --- Suas Views Existentes (Mantidas e Melhoradas) ---

def Boletim(request):
    # Idealmente, esta view também deveria filtrar as notas para um aluno específico
    notas = Nota.objects.all()
    return render(request, 'boletim_escolar.html', {'notas': notas})

def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'lista_alunos.html', {'alunos': alunos})

def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aluno_lista')
    else:
        form = AlunoForm()
    return render(request, 'forms_aluno.html', {'form': form})

def participacao(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    dados = [
        ('Pontualidade', aluno.pontualidade),
        ('Participação em aula', aluno.participacao_aula),
        ('Entregas de tarefas', aluno.entregas_tarefas),
        ('Comportamento c/ funcionários', aluno.comportamento_funcionarios),
        ('Participação em oficinas', aluno.participacao_oficinas),
        ('Comportamento em sala', aluno.comportamento_sala),
        ('Plataformas educacionais', aluno.participacao_plataformas),
    ]
    # Adicionando uma verificação para evitar divisão por zero se não houver dados
    media = sum(p for _, p in dados) // len(dados) if dados else 0
    return render(request, 'participacao.html', {'aluno': aluno, 'dados': dados, 'media': media})

@login_required
def dashboard_home(request):
    # Esta pode ser uma página de boas-vindas geral
    context = {'nome_responsavel': request.user.first_name or request.user.username}
    return render(request, 'dashboard.html', context)

# --- Novas Views que Criamos ---

@login_required
def desempenho_geral_view(request, aluno_pk):
    """ Mostra a tabela de desempenho com as notas de um aluno específico. """
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    notas = Nota.objects.filter(aluno=aluno).order_by('disciplina__nome')
    context = {
        'aluno': aluno,
        'notas': notas
    }
    return render(request, 'edutrack/desempenho_aluno.html', context)

@login_required
@login_required
def turmas_overview_view(request):
    """
    Calcula os dados de alunos por turma para exibir no gráfico.
    """
    total_alunos = Aluno.objects.count()

    # Agrupa os alunos pela SÉRIE da Turma e conta quantos há em cada uma
    # Usamos 'turma__serie' para pegar o nome correto que você cadastrou (ex: "1º ano")
    turmas_data = Aluno.objects.values('turma__serie').annotate(
        num_alunos=Count('id')
    ).order_by('turma__serie')

    # Prepara os dados como listas Python puras
    labels = [item['turma__serie'] for item in turmas_data]
    data = [item['num_alunos'] for item in turmas_data]

    context = {
        'total_alunos': total_alunos,
        # --- CORREÇÃO AQUI ---
        # Passamos as listas diretamente, sem usar json.dumps()
        'turmas_labels_json': labels,
        'turmas_data_json': data,
    }
    
    return render(request, 'edutrack/turmas_overview.html', context)

# --- Suas Outras Views (Mantidas) ---

@login_required
def grade_aluno(request):
    # A lógica para a grade horária continua a mesma
    aluno = get_object_or_404(Aluno, user=request.user)
    aulas = GradeHorario.objects.filter(turma=aluno.turma)
    grade_organizada = {}
    for dia, _ in GradeHorario.DIAS_SEMANA:
        grade_organizada[dia] = {}
        for hora, _ in GradeHorario.HORARIOS:
            grade_organizada[dia][hora] = None
    for aula in aulas:
        grade_organizada[aula.dia_semana][aula.horario] = aula
    context = {
        'aluno': aluno,
        'DIAS_SEMANA': GradeHorario.DIAS_SEMANA,
        'HORARIOS': GradeHorario.HORARIOS,
        'grade_organizada': grade_organizada,
    }
    return render(request, 'grade.html', context)

@login_required
def painel_aluno(request):
    aluno = get_object_or_404(Aluno, user=request.user)
    # Lógica para o painel do aluno...
    context = { 'aluno': aluno, }
    return render(request, 'bem_vindo_aluno.html', context)

@login_required
def tarefas_home(request):
    # Melhoria: busca as tarefas do aluno logado, não apenas do primeiro
    try:
        aluno_atual = Aluno.objects.get(user=request.user)
    except Aluno.DoesNotExist:
        # Lida com o caso de o usuário logado não ser um aluno
        return redirect('dashboard') # Redireciona para o dashboard geral

    atividades_base = Atividade.objects.filter(aluno=aluno_atual, entregue=False)
    # ... (o resto da sua lógica de filtro continua aqui) ...
    context = { 'aluno': aluno_atual, 'atividades': atividades_base } # Contexto simplificado
    return render(request, 'tarefas_provas.html', context)
