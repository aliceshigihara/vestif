from django.db import models

# Se já tiverem outras classes aqui (como Usuario), mantenha elas!
# Adicione a NotaCorte no final:

class NotaCorte(models.Model):
    INSTITUICOES = [
        ('UFSC', 'UFSC'),
        ('IFC', 'IFC'),
        ('IFSC', 'IFSC'),
    ]

    instituicao = models.CharField(max_length=10, choices=INSTITUICOES)
    cidade = models.CharField(max_length=50)
    curso = models.CharField(max_length=100)
    turno = models.CharField(max_length=50)
    nota_corte = models.FloatField()
    vagas = models.FloatField()

    def __str__(self):
        return f"{self.instituicao} - {self.curso} ({self.cidade})"
    
    class Meta:
        ordering = ['instituicao', 'cidade', 'curso']