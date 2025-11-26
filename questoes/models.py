from django.db import models
from django.conf import settings


class Questao(models.Model):
    numero = models.IntegerField(db_index=True)
    enunciado = models.TextField()

    alternativa_01 = models.TextField(blank=True, null=True)
    alternativa_02 = models.TextField(blank=True, null=True)
    alternativa_04 = models.TextField(blank=True, null=True)
    alternativa_08 = models.TextField(blank=True, null=True)
    alternativa_16 = models.TextField(blank=True, null=True)
    alternativa_32 = models.TextField(blank=True, null=True)
    alternativa_64 = models.TextField(blank=True, null=True)

    resposta = models.CharField(max_length=20, blank=True, null=True)

    def alternativas_dict(self):
        return {
            "01": self.alternativa_01,
            "02": self.alternativa_02,
            "04": self.alternativa_04,
            "08": self.alternativa_08,
            "16": self.alternativa_16,
            "32": self.alternativa_32,
            "64": self.alternativa_64,

        }
    
    def __str__(Self):
        return f"Questao {self.numero}"

class Tentativa(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tentativas'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    qtd_questoes = models.PositiveIntegerField()
    pontuacao = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.pontuacao}/{self.total}"
