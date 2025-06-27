from django.db import models

class Turma(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Aviso(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='avisos')
    texto = models.CharField("Texto do aviso", max_length=255)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        return f"{self.turma.nome} - {self.texto[:30]}"

class Atividade(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='atividades')
    descricao = models.CharField("Descrição", max_length=200)
    data = models.DateTimeField("Data da atividade")
    entregue_porcentagem = models.PositiveIntegerField("Entregue (%)", default=0)
    alunos_ausentes = models.PositiveIntegerField("Alunos ausentes", default=0)

    def __str__(self):
        return f"{self.turma.nome} - {self.descricao}"

class Recado(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='recados')
    mensagem = models.TextField("Mensagem")
    enviado_em = models.DateTimeField("Enviado em", auto_now_add=True)

    def __str__(self):
        return f"{self.turma.nome} - Recado"
