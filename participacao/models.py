# participacao/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
