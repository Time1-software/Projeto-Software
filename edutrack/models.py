from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Modelos de Suporte (Professor, Disciplina)
# ----------------------------------------------------

class Professor(models.Model):
    """Representa um professor, possivelmente ligado a um usuário do sistema."""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    nome_completo = models.CharField(max_length=100, verbose_name="Nome Completo")

    def __str__(self):
        return self.nome_completo

class Disciplina(models.Model):
    """Representa uma disciplina escolar."""
    nome = models.CharField(max_length=100, unique=True)



# Create your models here.
class Education(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

class Turma(models.Model):
    numero = models.CharField(max_length=20)
    serie = models.CharField(max_length=20)




class Aluno(models.Model):
    """Mantido o seu modelo de Aluno, pois é essencial."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField('Nome', max_length=100)
    matricula = models.CharField('Matrícula', max_length=20, unique=True)
    turma = models.CharField('Turma', max_length=50)

    pontualidade = models.PositiveIntegerField('Pontualidade (%)', default=0)
    participacao_aula = models.PositiveIntegerField('Participação em aula (%)', default=0)
    entregas_tarefas = models.PositiveIntegerField('Entregas de tarefas (%)', default=0)
    

    comportamento_funcionarios = models.PositiveIntegerField('Comportamento com funcionários (%)', default=0)
    participacao_oficinas = models.PositiveIntegerField('Participação em oficinas (%)', default=0)
    comportamento_sala = models.PositiveIntegerField('Comportamento em sala de aula (%)', default=0)
    participacao_plataformas = models.PositiveIntegerField('Participação em plataformas (%)', default=0)

    def __str__(self):
        return f'{self.nome} ({self.matricula})'

class Atividade(models.Model):

    class TipoAtividade(models.TextChoices):
        PROVA = 'PROVA', 'Prova'
        TRABALHO = 'TRABALHO', 'Trabalho'
        ATIVIDADE = 'ATIVIDADE', 'Atividade' # Para outros tipos de tarefas

    titulo = models.CharField(max_length=100, verbose_name="Título")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name="Disciplina")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name="Professor")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="atividades", verbose_name="Aluno")

    # Este campo é a chave para fazer os botões "Provas" e "Trabalhos" funcionarem!
    tipo = models.CharField(
        max_length=20,
        choices=TipoAtividade.choices,
        default=TipoAtividade.ATIVIDADE,
        verbose_name="Tipo de Atividade"
    )

    data_entrega = models.DateTimeField(verbose_name="Data e Hora de Entrega")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição/Observações")
    entregue = models.BooleanField(default=False, verbose_name="Entregue")

    class Meta:
        ordering = ['data_entrega'] # Ordena as tarefas pela data de entrega por padrão

    def __str__(self):
        return f'{self.titulo} - {self.aluno.nome}'

    @property
    def status(self):
        """
        Calcula o status da tarefa para fácil exibição no frontend.
        Retorna: 'hoje', 'essa_semana', 'proximas_semanas', 'atrasada'
        """
        if self.entregue:
            return 'entregue'

        hoje = timezone.now().date()
        data_entrega_date = self.data_entrega.date()

        if data_entrega_date < hoje:
            return 'atrasada'
        if data_entrega_date == hoje:
            return 'hoje'
        # Verifica se a data de entrega está na mesma semana (de hoje até o próximo domingo)
        if hoje < data_entrega_date <= hoje + timedelta(days=6 - hoje.weekday()):
            return 'essa_semana'
        
        return 'proximas_semanas'



# Modelos Secundários (Responsavel, Nota)
# ----------------------------------------------------

class Responsavel(models.Model):
    """Mantido o seu modelo de Responsável."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    filhos = models.ManyToManyField(Aluno, verbose_name="Filhos")
    telefone_contato = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno", null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name="Disciplina", null=True, blank=True)
    nota1 = models.FloatField(null=True, blank=True)
    nota2 = models.FloatField(null=True, blank=True)
    nota3 = models.FloatField(null=True, blank=True)
    recuperacao = models.FloatField("Recuperação", null=True, blank=True) 
    media = models.FloatField(null=True, blank=True, editable=False)

  
    def save(self, *args, **kwargs):
        if self.nota1 is not None and self.nota2 is not None and self.nota3 is not None:
            self.media = (self.nota1 + self.nota2 + self.nota3) / 3
        else:
            self.media = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Notas de {self.aluno.nome} em {self.disciplina.nome}'
    
class Calendario(models.Model):
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        return f"{self.atividade} - {self.data}"


class Resumo(models.Model):
    disciplina = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    links = models.URLField(blank=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class ConteudoDia(models.Model):
    disciplina = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    links = models.URLField(blank=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Quiz(models.Model):
    disciplina = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    ranking = models.TextField(blank=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Relatorio(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE, null=True, blank=True)
    comentarios = models.TextField()
    criado_por = models.ForeignKey(Professor, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório de {self.aluno}"


class Chat(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_enviadas_chat")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_recebidas_chat")
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remetente} → {self.destinatario}"



class GradeHorario(models.Model):
    DIAS_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
    ]

    HORARIOS = [
        ('1', '08:00 - 09:00'),
        ('2', '09:00 - 10:00'),
        ('3', '10:00 - 11:00'),
        ('4', '11:00 - 12:00'),
        ('5', '13:00 - 14:00'),
        ('6', '14:00 - 15:00'),
        ('7', '15:00 - 16:00'),
    ]

    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    horario = models.CharField(max_length=1, choices=HORARIOS)
    disciplina = models.CharField(max_length=100)
    sala = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['dia_semana', 'horario']
        verbose_name = 'Grade de Horário'
        verbose_name_plural = 'Grades de Horário'
        constraints = [
            models.UniqueConstraint(fields=['turma', 'dia_semana', 'horario'], name='unique_grade')
        ]

    def __str__(self):
        return f"{self.get_dia_semana_display()} {self.get_horario_display()} - {self.disciplina} ({self.turma})"

#LOGIN

CATEGORIAS = [
    ('aluno', 'Aluno(a)'),
    ('professor', 'Professor(a)'),
    ('responsavel', 'Responsável'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    def __str__(self):
        return f"{self.user.email} – {self.get_categoria_display()}"
