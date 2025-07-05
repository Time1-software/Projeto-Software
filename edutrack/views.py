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
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomSignupForm
from django.http import JsonResponse, HttpResponseBadRequest
import calendar
import unicodedata
from datetime import date
from django.shortcuts import render
from .models import Tarefa
from datetime import date
from .forms import TarefaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

# Area Usuario
@login_required
def perfil_usuario(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, "Perfil não encontrado. Entre em contato com o administrador.")
        return redirect('logout')

    if request.method == 'POST':
        campo = request.POST.get('campo')
        valor = request.POST.get('valor')
        aluno_id = request.POST.get('id')

        # Se for edição de aluno por responsável
        if aluno_id and profile.categoria == 'responsavel':
            try:
                aluno_profile = Profile.objects.get(id=aluno_id, responsavel=request.user)
                user = aluno_profile.user

                if campo == 'nome':
                    user.first_name = valor
                    user.save()
                elif campo == 'senha':
                    user.set_password(valor)
                    user.save()
                else:
                    return JsonResponse({'erro': 'Campo inválido'}, status=400)

                return JsonResponse({'sucesso': True})
            except Exception as e:
                return JsonResponse({'erro': str(e)}, status=500)

        # Edição do próprio usuário
        if campo == 'nome':
            request.user.first_name = valor
            request.user.save()
            return JsonResponse({'sucesso': True})
        elif campo == 'senha':
            request.user.set_password(valor)
            request.user.save()
            return JsonResponse({'sucesso': True})
        else:
            return JsonResponse({'erro': 'Campo inválido'}, status=400)

    # GET normal
    responsavel = getattr(profile, 'responsavel', None)
    dependentes = Profile.objects.filter(responsavel=request.user) if profile.categoria == 'responsavel' else []

    context = {
        'nome_responsavel': request.user.first_name or request.user.username,
        'profile': profile,
        'responsavel': responsavel,
        'categoria': profile.categoria,
        'email': request.user.email,
        'nome': request.user.first_name or request.user.email,
        'alunos': dependentes,
    }

    return render(request, 'perfil_usuario.html', context)


@csrf_exempt
def editar_aluno_por_responsavel(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('id')
        campo = request.POST.get('campo')
        valor = request.POST.get('valor')

        try:
            aluno = Profile.objects.get(id=aluno_id)
            user = aluno.user

            if campo == 'nome':
                user.first_name = valor
                user.save()
            elif campo == 'senha':
                user.set_password(valor)
                user.save()
            else:
                return JsonResponse({'erro': 'Campo inválido'}, status=400)

            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

    return HttpResponse(status=405)

@login_required
def vincular_responsavel(request):
    aluno_profile = getattr(request.user, 'profile', None)

    if not aluno_profile or aluno_profile.categoria != 'aluno':
        return render(request, 'vincular_responsavel.html', {
            'erro': 'Apenas alunos podem vincular um responsável.'
        })

    if request.method == 'POST':
        email = request.POST.get('email_responsavel')

        try:
            responsavel_user = User.objects.get(email=email)
            responsavel_profile = getattr(responsavel_user, 'profile', None)

            if not responsavel_profile or responsavel_profile.categoria != 'responsavel':
                return render(request, 'vincular_responsavel.html', {
                    'erro': 'O usuário informado não é um responsável válido.'
                })

            aluno_profile.responsavel = responsavel_user
            aluno_profile.save()

            return render(request, 'vincular_responsavel.html', {
                'sucesso': 'Responsável vinculado com sucesso!'
            })

        except User.DoesNotExist:
            return render(request, 'vincular_responsavel.html', {
                'erro': 'Nenhum usuário encontrado com esse e-mail.'
            })

    return render(request, 'vincular_responsavel.html')

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