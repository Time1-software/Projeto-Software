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

    def __str__(self):
        return self.nome



class Aluno(models.Model):
    """Mantido o seu modelo de Aluno, pois é essencial."""
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

class Education(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

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
    """Seu modelo de Nota foi mantido e levemente melhorado."""
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno", null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name="Disciplina", null=True, blank=True)
    nota1 = models.FloatField(null=True, blank=True)
    nota2 = models.FloatField(null=True, blank=True)
    nota3 = models.FloatField(null=True, blank=True)
    media = models.FloatField(null=True, blank=True, editable=False)

    # Métodos save e outros foram mantidos como você definiu.
    def save(self, *args, **kwargs):
        if self.nota1 is not None and self.nota2 is not None and self.nota3 is not None:
            self.media = (self.nota1 + self.nota2 + self.nota3) / 3
        else:
            self.media = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Notas de {self.aluno.nome} em {self.disciplina.nome}'

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, related_name='mensagens_enviadas', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='mensagens_recebidas', on_delete=models.CASCADE)
    assunto = models.CharField(max_length=255)
    corpo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"De: {self.remetente.username} | Para: {self.destinatario.username}"