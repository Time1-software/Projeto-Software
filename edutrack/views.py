import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from .forms import AlunoForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomSignupForm



import calendar
import unicodedata
from datetime import date
from django.shortcuts import render
from .models import Tarefa
from datetime import date
from .forms import TarefaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
def desempenho_geral_view(request, aluno_pk):

    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    notas = Nota.objects.filter(aluno=aluno).order_by('disciplina__nome')

    context = {
        'aluno': aluno,
        'notas': notas
    }
    
    return render(request, 'dashboard_pais.html', context)

#LOGIN


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = False

    def get_success_url(self):
        cat = self.request.user.profile.categoria
        mapping = {
            'aluno':        'painelAluno',
            'professor':    'bem_vindo_professor',
            'responsavel':  'bem_vindo_pai',
            'administrador':'bem_vindo_adm',
        }
        # se não achar categoria, volta para login
        return reverse_lazy(mapping.get(cat, 'login'))

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('signup-success')

class SignupSuccessView(TemplateView):
    template_name = 'signup_success.html'

class BemvindoAlunoView(TemplateView):
    template_name = 'painel_aluno.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['email'] = self.request.user.email
        return ctx

class BemvindoProfessorView(TemplateView):
    template_name = 'bem_vindo_professor.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['email'] = self.request.user.email
        return ctx

class BemvindoPaiView(TemplateView):
    template_name = 'bem_vindo_pai.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['email'] = self.request.user.email
        return ctx

class BemvindoAdmView(TemplateView):
    template_name = 'bem_vindo_adm.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['email'] = self.request.user.email
        return ctx


#Calendario
def remove_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

class CalendarioPT(calendar.HTMLCalendar):
    def __init__(self, tarefas, ano, mes):
        super().__init__(firstweekday=0)
        self.tarefas_por_dia = self._organiza_tarefas(tarefas)
        self.ano = ano
        self.mes = mes

    def _organiza_tarefas(self, tarefas):
        tarefas_por_dia = {}
        for tarefa in tarefas:
            dia = tarefa.data.day
            if dia not in tarefas_por_dia:
                tarefas_por_dia[dia] = []
            tarefas_por_dia[dia].append(tarefa)
        return tarefas_por_dia



    # Dentro da classe CalendarioPT
    def formatday(self, day, weekday):
        if day == 0:
            return '<td></td>'

        hoje = date.today()
        classe_extra = "hoje" if (self.ano == hoje.year and self.mes == hoje.month and day == hoje.day) else ""

        tarefas = self.tarefas_por_dia.get(day, [])
        html = f'<div class="dia-num">{day}</div>'

        for t in tarefas:
            tipo_original = t.tipo or ''
            tipo = remove_acentos(tipo_original.strip().upper())

            if tipo == 'PROVA':
                cor = 'vermelho'
            elif tipo == 'TRABALHO':
                cor = 'amarelo'
            elif tipo == 'TESTE':
                cor = 'laranja'
            elif tipo == 'APRESENTACAO':
                cor = 'azul'
            else:
                cor = 'azul'

            turma = f'{t.turma.serie} - {t.turma.numero}'
            html += f'''
                <div class="tarefa {cor}" 
                    data-titulo="{t.titulo}"
                    data-tipo="{t.tipo}"
                    data-data="{t.data.strftime('%d/%m/%Y')}"
                    data-descricao="{t.descricao}"
                    data-autor="{t.autor.get_full_name() if t.autor else 'Desconhecido'}"
                    data-turma="{turma}">
                    {t.titulo}
                </div>
            '''

        return f'<td class="dia {classe_extra}">{html}</td>'

    def formatmonthname(self, theyear, themonth, withyear=True):
        meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        nome = meses_pt[themonth - 1]
        return f'<tr><th colspan="7" class="mes">{nome} {theyear}</th></tr>'

    def formatweekday(self, day):
        dias_pt = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        return f'<th>{dias_pt[day]}</th>'


def calendario_view(request):
    hoje = date.today()
    ano = int(request.GET.get('ano', hoje.year))
    mes = int(request.GET.get('mes', hoje.month))

    tarefas = Tarefa.objects.filter(data__year=ano, data__month=mes)
    cal = CalendarioPT(tarefas, ano, mes).formatmonth(ano, mes)

    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano

    if mes == 12:
        mes_proximo = 1
        ano_proximo = ano + 1
    else:
        mes_proximo = mes + 1
        ano_proximo = ano

    return render(request, 'calendario.html', {
        'calendario': cal,
        'ano': ano,
        'mes': mes,
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_proximo': mes_proximo,
        'ano_proximo': ano_proximo,
    })


@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.autor = request.user
            tarefa.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('criar_tarefa')
    else:
        form = TarefaForm()

    return render(request, 'criar_tarefa.html', {'form': form})
