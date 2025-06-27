from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.
class Education(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

class Nota(models.Model):
    disciplina = models.CharField(max_length=100)
    nota1 = models.FloatField(null=True, blank=True)
    nota2 = models.FloatField(null=True, blank=True)
    nota3 = models.FloatField(null=True, blank=True)
    media = models.FloatField(null=True, blank=True)
    recuperacao = models.FloatField(null=True, blank=True)
    
    def todas_notas_preenchidas(self):
        return self.nota1 is not None and self.nota2 is not None and self.nota3 is not None

    def calcular_media(self):
        if self.todas_notas_preenchidas():
            return (self.nota1 + self.nota2 + self.nota3) / 3
        return None

    def save(self, *args, **kwargs):
        self.media = self.calcular_media()
        self.recuperacao = self.media is not None and self.media < 7
        super().save(*args, **kwargs)

    def __str__(self):
        if self.media is not None:
            return f'{self.disciplina} - Média: {self.media:.2f}'
        else:
            return f'{self.disciplina} - Média: -'

# participacao/models.py


class Aluno(models.Model):
    nome = models.CharField('Nome', max_length=100)
    matricula = models.CharField('Matrícula', max_length=20, unique=True)
    turma = models.CharField('Turma', max_length=50)

    pontualidade = models.PositiveIntegerField(
        'Pontualidade (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    participacao_aula = models.PositiveIntegerField(
        'Participação em aula (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    entregas_tarefas = models.PositiveIntegerField(
        'Entregas de tarefas (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    comportamento_funcionarios = models.PositiveIntegerField(
        'Comportamento com funcionários (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    participacao_oficinas = models.PositiveIntegerField(
        'Participação em oficinas (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    comportamento_sala = models.PositiveIntegerField(
        'Comportamento em sala de aula (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    participacao_plataformas = models.PositiveIntegerField(
        'Participação em plataformas (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )

    def __str__(self):
        return f'{self.nome} ({self.matricula})'

class Responsavel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    filhos = models.ManyToManyField(Aluno, verbose_name="Filhos")
    telefone_contato = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Turma(models.Model):
    numero = models.CharField(max_length=20)
    serie = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.numero} - {self.serie}"


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    nome = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    prazo = models.DateField()
    anexos = models.FileField(upload_to='anexos/', blank=True, null=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Calendario(models.Model):
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        return f"{self.atividade} - {self.data}"


class Resumo(models.Model):
    disciplina = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    links = models.URLField(blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class ConteudoDia(models.Model):
    disciplina = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    links = models.URLField(blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Quiz(models.Model):
    disciplina = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    ranking = models.TextField(blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

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
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_enviadas")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_recebidas")
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remetente} → {self.destinatario}"


class GradeHorario(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    horario = models.CharField(max_length=100)

    def __str__(self):
        return f"Grade de {self.aluno}"
