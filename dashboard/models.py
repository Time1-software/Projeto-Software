from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Aluno(models.Model):
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()


    def __str__(self):
        return self.nome_completo


class Responsavel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    filhos = models.ManyToManyField(Aluno, verbose_name="Filhos")
    telefone_contato = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username