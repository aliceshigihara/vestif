from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum
import json
from .models import Questao, Tentativa, Prova, RespostaUsuario

# --- FUNÇÃO AUXILIAR DE CÁLCULO (Movida para fora das views para organização) ---
def calcular_pontuacao_ufsc(marcadas_str, resposta_correta_str):
    """
    Retorna a pontuação (0.0 a 1.0) para uma questão.
    """
    if not resposta_correta_str or not resposta_correta_str.isdigit():
        return 0.0

    soma_correta = int(resposta_correta_str)
    
    # Se o aluno não marcou nada
    if not marcadas_str:
        return 0.0

    marcadas_int = [int(x) for x in marcadas_str]
    soma_usuario = sum(marcadas_int)

    # Acerto total direto
    if soma_usuario == soma_correta:
        return 1.0

    # Lógica UFSC
    # Pesos possíveis: 1, 2, 4, 8, 16, 32, 64
    todos_pesos = [2**i for i in range(7)] 
    
    # Divide os pesos em corretos (gabarito) e incorretos
    itens_corretos = [p for p in todos_pesos if (p & soma_correta)]
    itens_incorretos = [p for p in todos_pesos if not (p & soma_correta)]
    
    # Conta quantos corretos e quantos errados o aluno marcou
    np = len(itens_corretos) # Número de proposições verdadeiras
    nt = len(itens_incorretos) # Número de proposições falsas (que não deveriam ser marcadas)
    
    npc = sum(1 for x in marcadas_int if x in itens_corretos) # Corretas marcadas pelo aluno
    npi = sum(1 for x in marcadas_int if x in itens_incorretos) # Incorretas marcadas pelo aluno
    
    if np == 0: return 0.0 # Proteção contra divisão por zero

    # Fórmula: P = (NPC/NP) - (NPI/NT)
    # Se NT for 0 (todas as opções são verdadeiras), a segunda parte é 0
    parte_acertos = npc / np
    parte_erros = (npi / nt) if nt > 0 else 0
    
    pontuacao = parte_acertos - parte_erros

    return max(0.0, round(pontuacao, 2)) # Nunca negativo, arredonda 2 casas


# --- VIEWS ---

@login_required
def menu_simulado(request):
    provas = Prova.objects.all().order_by('-ano')
    
    # Mágica: Pega todas as disciplinas únicas cadastradas no banco, em ordem alfabética
    todas_disciplinas = Questao.objects.values_list('disciplina', flat=True).distinct().order_by('disciplina')
    
    return render(request, 'menu.html', {
        'provas': provas,
        'disciplinas': todas_disciplinas # Enviando para o HTML
    })

@login_required
def iniciar_simulado(request):
    # Agora precisamos saber QUAL prova o usuário quer fazer
    prova_id = request.GET.get('prova_id')
    
    if not prova_id:
        # Se não tiver ID, redireciona pro menu ou pega a última
        return redirect('questoes:menu_simulado')

    prova = get_object_or_404(Prova, id=prova_id)
    
    # ORDENAÇÃO FIXA: .order_by('numero') tira a aleatorização
    questoes = prova.questao_set.all().order_by('numero')

    # Se quiser filtrar disciplina DENTRO da prova:
    disciplina_filtro = request.GET.get('disciplina')
    if disciplina_filtro:
        questoes = questoes.filter(disciplina=disciplina_filtro)

    codes = ["01", "02", "04", "08", "16", "32", "64"]

    return render(request, 'questoes/simulado.html', {
        'questoes': questoes,
        'prova': prova,
        'codes': codes,
        'disciplina_atual': disciplina_filtro or "Completa"
    })

@login_required
@require_POST
def corrigir_simulado(request, prova_id):
    dados = json.loads(request.body)
    respostas_usuario = dados.get("respostas", {})
    disciplina_filtro = dados.get("disciplina") # Recebe "PORTUGUÊS", "MATEMÁTICA" ou "Completa"
    
    prova = get_object_or_404(Prova, id=prova_id)
    
    # 1. Pega todas as questões da prova
    questoes_para_corrigir = prova.questao_set.all().order_by('numero')
    
    # 2. SE tiver filtro (e não for prova completa), filtra as questões
    if disciplina_filtro and disciplina_filtro not in ["Completa", "Geral", "None"]:
        questoes_para_corrigir = questoes_para_corrigir.filter(disciplina=disciplina_filtro)
    
    pontuacao_total_acumulada = 0.0
    
    # A Tentativa agora terá apenas o total daquela matéria
    total_questoes = questoes_para_corrigir.count()

    tentativa = Tentativa.objects.create(
        usuario=request.user,
        prova=prova,
        qtd_questoes=total_questoes,
        pontuacao=0,
        total=total_questoes 
    )

    # Itera APENAS sobre as questões da matéria escolhida
    for questao in questoes_para_corrigir:
        numero_str = str(questao.numero)
        marcadas = respostas_usuario.get(numero_str, [])
        
        nota_questao = 0.0
        acertou_totalmente = False
        
        if questao.resposta and questao.resposta.isdigit():
            nota_questao = calcular_pontuacao_ufsc(marcadas, questao.resposta)
            if nota_questao == 1.0:
                acertou_totalmente = True
        
        pontuacao_total_acumulada += nota_questao
        
        # Salva a resposta
        RespostaUsuario.objects.create(
            tentativa=tentativa,
            questao=questao,
            resposta_marcada=json.dumps(marcadas),
            acertou_totalmente=acertou_totalmente,
            pontos_obtidos=nota_questao
        )

    tentativa.pontuacao = round(pontuacao_total_acumulada, 2)
    tentativa.save()

    return redirect("questoes:correcao", tentativa_id=tentativa.id)

@login_required
def correcao(request, tentativa_id):
    tentativa = get_object_or_404(Tentativa, id=tentativa_id, usuario=request.user)
    
    # Recupera as respostas detalhadas para exibir no template
    respostas_detalhadas = tentativa.respostas.all().select_related('questao').order_by('questao__numero')

    return render(request, "questoes/correcao.html", {
        "tentativa": tentativa,
        "respostas": respostas_detalhadas
    })

@login_required
def historico(request):
    # Pegamos as tentativas ordenadas da MAIS ANTIGA para a NOVA (para o gráfico ir da esquerda p/ direita)
    tentativas = Tentativa.objects.filter(usuario=request.user).order_by('criado_em')
    
    # Preparamos os dados para o gráfico
    datas = [t.criado_em.strftime("%d/%m %H:%M") for t in tentativas]
    notas = [t.pontuacao for t in tentativas]
    
    # Para a tabela lá embaixo, a gente inverte a ordem (mais recente primeiro)
    tentativas_reverso = tentativas.reverse()

    return render(request, 'historico.html', {
        'tentativas': tentativas_reverso,
        'grafico_datas': datas,  # Lista de datas
        'grafico_notas': notas   # Lista de notas
    })