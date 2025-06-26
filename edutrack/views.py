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