from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from .forms import AlunoForm
from django.contrib.auth.decorators import login_required
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

def professor(request):
   return render(request, 'professor.html')


def painel_turmas(request):
   return render(request, 'painel_turmas.html')


def resumo(request):
   
   return render(request, 'resumo.html')

def turma_presenca(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    # busca todos os Aluno cujo campo `turma` bate com o número da turma
    alunos = Aluno.objects.filter(turma=turma.numero)
    return render(request, 'turma_presenca.html', {
        'turma': turma,
        'alunos': alunos,
    })


def turma_tarefas(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    tarefas = Atividade.objects.filter(turma=turma).order_by('-prazo')
    turma    = get_object_or_404(Turma, pk=turma_id)
    tarefas  = Atividade.objects.filter(turma=turma).order_by('-prazo')
    days     = [1,2,3,4,5]         # segunda=1 ... sexta=5
    # ... seu POST para criar tarefas ...
    if request.method == 'POST':
        # cria nova atividade a partir do formulário
        descricao = request.POST.get('descricao', '').strip()
        prazo     = request.POST.get('prazo') 
        if descricao and prazo:
            Atividade.objects.create(
                nome=descricao,
                titulo=descricao,
                descricao=descricao,
                prazo=prazo,
                turma=turma,
                # se você tiver um professor logado:
                # professor=request.user.professor
            )
        return redirect('turma_tarefas', turma_id=turma.id)
    # em edutrack/views.py, dentro de turma_tarefas:
   
    return render(request, 'turma_tarefas.html', {
        'turma': turma,
        'tarefas': tarefas,
        'days': days,
    })
def turma_diario(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    entradas = ConteudoDia.objects.filter(turma=turma).order_by('-id')
    if request.method == 'POST':
        data     = request.POST.get('data')
        conteudo = request.POST.get('conteudo', '').strip()
        if data and conteudo:
            # Como seu model ConteudoDia não tem campo 'descricao',
            # vamos reaproveitar o campo 'titulo' para guardar o texto
            ConteudoDia.objects.create(
                disciplina='',      # você pode ajustar
                titulo=conteudo,    # texto da entrada
                links='',
                turma=turma
            )
        return redirect('turma_diario', turma_id=turma.id)

    return render(request, 'turma_diario.html', {
        'turma': turma,
        'entradas': entradas,
    })