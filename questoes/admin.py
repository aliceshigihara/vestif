from django.contrib import admin

from django.contrib import admin
from .models import Questao, TextoApoio, Tentativa, Prova, RespostaUsuario

admin.site.register(Prova)
admin.site.register(Questao)
admin.site.register(Tentativa)
admin.site.register(RespostaUsuario)