import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from .forms import AlunoForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

# Create your views here.
#Boletim
def Boletim(request):
    notas = Nota.objects.all()
    for nota in notas:
        nota.tem_todas_notas = (
            nota.nota1 is not None and nota.nota2 is not None and nota.nota3 is not None
        )
    return render(request, 'boletim_escolar.html', {'notas': notas})

#Participação
def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'lista_alunos.html', {
        'alunos': alunos
    })

def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aluno_lista')
    else:
        form = AlunoForm()
    return render(request, 'forms_aluno.html', {
        'form': form
    })

def participacao(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    # monta a lista de métricas puxando do próprio model
    dados = [
        ('Pontualidade', aluno.pontualidade),
        ('Participação em aula', aluno.participacao_aula),
        ('Entregas de tarefas', aluno.entregas_tarefas),
        ('Comportamento c/ funcionários', aluno.comportamento_funcionarios),
        ('Participação em oficinas', aluno.participacao_oficinas),
        ('Comportamento em sala', aluno.comportamento_sala),
        ('Plataformas educacionais', aluno.participacao_plataformas),
        
    ]
    media = sum(p for _, p in dados) // len(dados)
    return render(request, 'participacao.html', {
        'aluno': aluno,
        'dados': dados,
        'media': media,
    })


@login_required
def dashboard_home(request):

    context = {
        'nome_responsavel': request.user.first_name or request.user.username
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def grade_aluno(request):
    aluno = get_object_or_404(Aluno, user=request.user)
    #grade = GradeHorario.objects.filter(turma=aluno.turma).order_by('dia_semana', 'horario')
    
     # Busca todas as aulas da turma
    aulas = GradeHorario.objects.filter(turma=aluno.turma)

    # Organiza por [dia][horario]
    grade_organizada = {}
    for dia, _ in GradeHorario.DIAS_SEMANA:
        grade_organizada[dia] = {}
        for hora, _ in GradeHorario.HORARIOS:
            grade_organizada[dia][hora] = None

    for aula in aulas:
        grade_organizada[aula.dia_semana][aula.horario] = aula

    return render(request, 'grade.html', {
        'aluno': aluno,
        'DIAS_SEMANA': GradeHorario.DIAS_SEMANA,
        'HORARIOS': GradeHorario.HORARIOS,
        'grade_organizada': grade_organizada,
    })

@login_required
def painel_aluno(request):
    aluno = get_object_or_404(Aluno, user=request.user)

    #CARD GRADE-HORÁRIA
    # Dia da semana atual (ex: 'SEG', 'TER'...)
    dia_semana_hoje = datetime.datetime.today().strftime('%a').upper()

    # Mapeia 'MON' para 'SEG', etc
    tradutor_dias = {
        'MON': 'SEG',
        'TUE': 'TER',
        'WED': 'QUA',
        'THU': 'QUI',
        'FRI': 'SEX',
    }

    dia_chave = tradutor_dias.get(dia_semana_hoje, None)

    aulas_hoje = []
    if dia_chave:
        aulas_hoje = GradeHorario.objects.filter(turma=aluno.turma, dia_semana=dia_chave).order_by('horario')

    #notificações rápidas
    atividades_hoje = [
        a for a in Atividade.objects.filter(aluno=aluno, entregue=False)
        if a.status == 'hoje'
    ]

  
    # Dados para o resumo do dia
    tem_tarefas_hoje = len(atividades_hoje) > 0
    qtd_tarefas_hoje = len(atividades_hoje)

    context = {
        'aluno': aluno,
        'aulas_hoje': aulas_hoje,
        'atividades_hoje': atividades_hoje,
        'tem_tarefas_hoje': tem_tarefas_hoje,
        'qtd_tarefas_hoje': qtd_tarefas_hoje,
    }

    return render(request, 'bem_vindo_aluno.html', context)

def tarefas_home(request):

    aluno_atual = Aluno.objects.first() 

    atividades_base = Atividade.objects.filter(aluno=aluno_atual, entregue=False)


    filtro_tipo = request.GET.get('tipo', None)
    if filtro_tipo in ['PROVA', 'TRABALHO']:
        atividades_filtradas = atividades_base.filter(tipo=filtro_tipo)
    else:
        atividades_filtradas = atividades_base

    context = {
        'tarefas_hoje': [t for t in atividades_filtradas if t.status == 'hoje'],
        'tarefas_semana': [t for t in atividades_filtradas if t.status == 'essa_semana'],
        'tarefas_futuras': [t for t in atividades_filtradas if t.status == 'proximas_semanas'],
        'tarefas_atrasadas': [t for t in atividades_filtradas if t.status == 'atrasada'],
        'aluno': aluno_atual,
        'request': request,
    }


    return render(request, 'tarefas_provas.html', context)


def pagina_de_tarefas(request):

    aluno_atual = Aluno.objects.first() 
    

    atividades_pendentes = Atividade.objects.filter(aluno=aluno_atual, entregue=False)


    filtro_tipo = request.GET.get('tipo') 
    if filtro_tipo in ['PROVA', 'TRABALHO']:
        atividades_pendentes = atividades_pendentes.filter(tipo=filtro_tipo)

    context = {
        'tarefas_hoje': [t for t in atividades_pendentes if t.status == 'hoje'],
        'tarefas_semana': [t for t in atividades_pendentes if t.status == 'essa_semana'],
        'tarefas_futuras': [t for t in atividades_pendentes if t.status == 'proximas_semanas'],
        'tarefas_atrasadas': [t for t in atividades_pendentes if t.status == 'atrasada'],
        'aluno': aluno_atual,
    }

    return render(request, 'tarefas_provas.html', context)

@login_required 
def dashboard_pais_view(request):
    """
    Esta view mostra um dashboard para o pai/mãe logado,
    exibindo os cartões para cada filho associado.
    """
    try:
        responsavel = Responsavel.objects.get(user=request.user)

        lista_de_alunos = responsavel.filhos.all()
    except Responsavel.DoesNotExist:

        lista_de_alunos = []

    context = {
        'alunos': lista_de_alunos,
    }
    
    return render(request, 'dashboard_pais.html', context)