from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Questao, Tentativa
import random
import json



@login_required
def iniciar_simulado(request):
    qtd = int(request.GET.get('qtd', 10))
    questoes = list(Questao.objects.all())
    random.shuffle(questoes)
    selecionadas = questoes[:qtd]

    codes = ["01", "02", "04", "08", "16", "32", "64"]

    return render(request, 'questoes/simulado.html', {
        'questoes': selecionadas,
        'qtd': qtd,
        'codes': codes
    })



@login_required
def corrigir_simulado(request):
    if request.method == 'POST':

        dados = json.loads(request.body)
        respostas_usuario = dados.get("respostas", {})

        acertos = 0
        total = Questao.objects.count()

        # Corrigir agora usando respostas_usuario corretamente
        for numero, marcadas in respostas_usuario.items():
            try:
                q = Questao.objects.get(numero=int(numero))

                # Se a resposta é bitwise (01,02,04...)
                if q.resposta.isdigit():
                    soma_usuario = sum(int(x) for x in marcadas)
                    soma_correta = int(q.resposta)
                    if soma_usuario == soma_correta:
                        acertos += 1

                else:
                    # Caso resposta seja "A,B,D"
                    correta = q.resposta.split(",")
                    if sorted(marcadas) == sorted(correta):
                        acertos += 1

            except Questao.DoesNotExist:
                pass

        tentativa = Tentativa.objects.create(
            usuario=request.user,
            qtd_questoes=len(respostas_usuario),
            pontuacao=acertos,
            total=total
        )

        return redirect("questoes:correcao", tentativa_id=tentativa.id)

    return redirect("questoes:simulado")

@login_required
def historico(request):
    tentativas = Tentativa.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'questoes/historico.html', {'tentativas': tentativas})



def correcao(request, tentativa_id):
    tentativa = get_object_or_404(Tentativa, id=tentativa_id)

    return render(request, "questoes/correcao.html", {
        "tentativa": tentativa
    })

def calcular_pontuacao_ufsc(marcadas, soma_correta):
    """
    marcadas = lista de strings ['01', '08', ...]
    soma_correta = int (ex: 9)
    """

    # Converter strings para inteiros
    marcadas_int = [int(x) for x in marcadas]

    # Soma do candidato
    soma_usuario = sum(marcadas_int)

    # Se acertou exatamente:
    if soma_usuario == soma_correta:
        return soma_correta  # ganha pontuação cheia

    # Calcular quantos pontos corretos existem (somatória correta)
    pontos_corretos = soma_correta

    # Todos os 7 pesos possíveis
    todos = [1, 2, 4, 8, 16, 32, 64]

    # Somar pesos errados
    pesos_errados = [x for x in todos if x not in [int(c) for c in marcadas_int] and x not in [int(c) for c in marcadas_int]]

    # Soma total errada possível
    soma_errada_total = sum([x for x in todos if x not in [int(c) for c in marcadas_int]])

    # Calcular quantos corretos o candidato marcou
    corretos_marcados = sum([x for x in marcadas_int if x & soma_correta == x])

    # Calcular quantos errados o candidato marcou
    errados_marcados = soma_usuario - corretos_marcados

    # Evitar divisão por zero
    if pontos_corretos == 0:
        return 0

    # Fórmula UFSC
    pontuacao = (corretos_marcados / pontos_corretos) - (errados_marcados / soma_errada_total)

    # Nunca deixar negativo
    return max(0, pontuacao * soma_correta)
