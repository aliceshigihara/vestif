from django.db import models
from django.conf import settings

class Prova(models.Model):
    titulo = models.CharField(max_length=200)
    ano = models.IntegerField()
    # outros campos...
    def __str__(self):
        return f"{self.titulo} - {self.ano}"

class TextoApoio(models.Model):
    titulo = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='textos_apoio_img/', blank=True, null=True)
    conteudo = models.TextField(blank=True, null=True)
    fonte = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.titulo

class Questao(models.Model):
    prova = models.ForeignKey('Prova', on_delete=models.CASCADE, null=True, blank=True)
    numero = models.IntegerField()
    disciplina = models.CharField(max_length=100)
    enunciado = models.TextField()
    resposta = models.CharField(max_length=10) # Gabarito
    
    # --- ESTAVA FALTANDO ISSO AQUI ---
    texto_01 = models.TextField(blank=True, null=True)
    texto_02 = models.TextField(blank=True, null=True)
    texto_04 = models.TextField(blank=True, null=True)
    texto_08 = models.TextField(blank=True, null=True)
    texto_16 = models.TextField(blank=True, null=True)
    texto_32 = models.TextField(blank=True, null=True)
    texto_64 = models.TextField(blank=True, null=True)
    # ---------------------------------

    imagem = models.ImageField(upload_to='questoes/', blank=True, null=True)

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"{self.disciplina} - Q{self.numero}"

    @property
    def alternativas_dict(self):
        """ Retorna dict para o template apenas com as preenchidas """
        todas = {
            "01": self.texto_01,
            "02": self.texto_02,
            "04": self.texto_04,
            "08": self.texto_08,
            "16": self.texto_16,
            "32": self.texto_32,
            "64": self.texto_64,
        }
        # Filtra removendo as vazias
        return {k: v for k, v in todas.items() if v}


    @property
    def alternativas_dict(self):

        todas = {
            "01": self.texto_01,
            "02": self.texto_02,
            "04": self.texto_04,
            "08": self.texto_08,
            "16": self.texto_16,
            "32": self.texto_32,
            "64": self.texto_64,
        }

        return {k: v for k, v in todas.items() if v}
        
    def alternativas_dict(self):
        return {
            "01": self.texto_01,
            "02": self.texto_02,
            "04": self.texto_04,
            "08": self.texto_08,
            "16": self.texto_16,
            "32": self.texto_32,
            "64": self.texto_64,
        }
    
    def __str__(self):
        return f"Questao {self.numero} - {self.disciplina}"

class Meta:
        ordering = ['numero']

class Tentativa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    qtd_questoes = models.IntegerField()
    pontuacao = models.FloatField(default=0.0) # Float para aceitar parciais
    total = models.IntegerField() # Valor total da prova (ex: 10.0 ou número de questões)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.pontuacao}/{self.total}"

class RespostaUsuario(models.Model):
    tentativa = models.ForeignKey(Tentativa, on_delete=models.CASCADE, related_name='respostas')
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    resposta_marcada = models.TextField() # Salva JSON: '["01", "04"]'
    acertou_totalmente = models.BooleanField(default=False)
    pontos_obtidos = models.FloatField(default=0.0)