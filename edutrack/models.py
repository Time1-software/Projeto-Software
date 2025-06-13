from django.db import models

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