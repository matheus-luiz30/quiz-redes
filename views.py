import time

from flask import render_template, request, session, redirect, url_for

from app import app
from classes.class_jogador import Jogador
from classes.class_pergunta import Pergunta
from reutilizavel.validacao_dados import (
    VINCULOS, FAIXAS_ETARIAS, apelido_e_valido, vinculo_e_valido, faixa_etaria_e_valida,
    gerar_apelido_padrao, normalizar_origem,
)
from reutilizavel.perfil_jogador import calcular_perfil
from reutilizavel.filtro_apelido import apelido_e_ofensivo
from servicos.motor_quiz import MotorQuiz


@app.before_request
def tornar_session_permanente():
    # Usa a duração definida em app.permanent_session_lifetime (app.py)
    session.permanent = True


@app.route("/")
def index():
    # A origem fica na session (e não só na URL) para sobreviver a um clique no
    # logo, a um erro no formulário e ao "Jogar de novo".
    if "origem" in request.args:
        session["origem"] = normalizar_origem(request.args["origem"])

    return mostrar_tela_inicial()


# Tela inicial com as opções de perfil. Em caso de erro, recebe o que a pessoa já
# tinha preenchido (apelido, vinculo, faixa_etaria, erro) para não perder nada.
def mostrar_tela_inicial(**preenchido):
    return render_template(
        "nome.html", vinculos=VINCULOS, faixas_etarias=FAIXAS_ETARIAS, **preenchido
    )


@app.route("/ranking")
def ranking():
    top_resultados = Jogador.obter_ranking(10)
    return render_template("ranking.html", top_resultados=top_resultados)


@app.route("/jogar-novo")
def jogar_novo():
    # Origem e tentativa sobrevivem ao "Jogar de novo": o resto da session é zerado
    origem = session.get("origem", "direto")
    tentativa = session.get("tentativa", 0)
    session.clear()
    session.permanent = True
    session["origem"] = origem
    session["tentativa"] = tentativa
    return redirect(url_for("index"))


@app.route("/comecar", methods=["POST"])
def comecar():
    apelido = request.form.get("apelido", "").strip()
    vinculo = request.form.get("vinculo", "")
    faixa_etaria = request.form.get("faixa_etaria", "")
    preenchido = {"apelido": apelido, "vinculo": vinculo, "faixa_etaria": faixa_etaria}

    if not apelido_e_valido(apelido):
        return mostrar_tela_inicial(
            erro="Apelido inválido: use de 2 a 20 letras, números, espaço, _ - ou ponto.",
            **preenchido,
        )

    if not vinculo_e_valido(vinculo):
        return mostrar_tela_inicial(erro="Escolha o seu vínculo para começar.", **preenchido)

    if not faixa_etaria_e_valida(faixa_etaria):
        return mostrar_tela_inicial(erro="Escolha a sua faixa etária para começar.", **preenchido)

    # Apelido ofensivo não gera erro na tela: troca em silêncio pelo padrão
    if apelido == "" or apelido_e_ofensivo(apelido):
        apelido = gerar_apelido_padrao()

    nome = apelido
    jogador = Jogador(nome, vinculo, faixa_etaria)
    jogador_id = jogador.salvar_novo_no_banco()

    session["jogador_id"] = jogador_id
    # Conta cada partida iniciada neste navegador (1 = primeira vez). Quem joga de
    # novo já conhece as perguntas; a análise pode filtrar por tentativa = 1.
    session["tentativa"] = session.get("tentativa", 0) + 1
    session["resultado_id"] = Jogador.iniciar_resultado(
        jogador_id, session.get("origem", "direto"), session["tentativa"]
    )
    session["nome"] = nome
    session["pergunta_atual"] = 0
    session["pontuacao"] = 0
    session["acertos"] = 0
    session["inicio_tempo"] = time.time()
    session["resultado_salvo"] = False

    return redirect(url_for("pergunta"))


@app.route("/pergunta")
def pergunta():
    if "resultado_id" not in session:
        return redirect(url_for("index"))

    perguntas = Pergunta.buscar_todas()
    indice = session["pergunta_atual"]

    if indice >= len(perguntas):
        if not session["resultado_salvo"]:
            session["tempo_total"] = time.time() - session["inicio_tempo"]
            Jogador.finalizar_resultado(
                session["resultado_id"], session["pontuacao"], session["acertos"], session["tempo_total"]
            )
            session["resultado_salvo"] = True

        titulo, modo = calcular_perfil(session["acertos"], len(perguntas), session["tempo_total"])

        return render_template(
            "resultado.html",
            nome=session["nome"],
            pontuacao=session["pontuacao"],
            acertos=session["acertos"],
            total_perguntas=len(perguntas),
            tempo_total=session["tempo_total"],
            titulo=titulo,
            modo=modo,
            top_resultados=Jogador.obter_ranking(10),
            resultado_id=session["resultado_id"],
        )

    # Só reinicia o cronômetro quando a pergunta muda: recarregar a página (F5)
    # não zera o tempo de resposta.
    if session.get("indice_cronometrado") != indice:
        session["indice_cronometrado"] = indice
        session["inicio_pergunta"] = time.time()

    pergunta_atual = perguntas[indice]
    letras = ["a", "b", "c", "d"]
    alternativas_com_letra = list(zip(letras, pergunta_atual.alternativas))

    return render_template(
        "pergunta.html",
        pergunta=pergunta_atual,
        alternativas_com_letra=alternativas_com_letra,
        pontuacao=session["pontuacao"],
        acertos=session["acertos"],
    )


@app.route("/responder", methods=["POST"])
def responder():
    if "resultado_id" not in session:
        return redirect(url_for("index"))

    # A letra vai para o banco (resposta_dada): não confia no formulário, que pode
    # ter sido adulterado ou chegado sem o campo.
    resposta_escolhida = request.form.get("resposta", "").strip().lower()
    if resposta_escolhida not in ["a", "b", "c", "d"]:
        return redirect(url_for("pergunta"))

    perguntas = Pergunta.buscar_todas()
    indice = session["pergunta_atual"]

    if indice >= len(perguntas):
        return redirect(url_for("pergunta"))

    pergunta_atual = perguntas[indice]

    # Envio duplicado (clique duplo, voltar do navegador + reenviar): o formulário
    # traz o id da pergunta que estava na tela; se não for a atual, ignora.
    if request.form.get("pergunta_id") != str(pergunta_atual.id):
        return redirect(url_for("pergunta"))

    jogador = Jogador(session["nome"])
    motor = MotorQuiz(jogador, [pergunta_atual])

    acertou = motor.verificar_resposta(pergunta_atual, resposta_escolhida)
    comentario = motor.comentar_host(acertou)

    tempo_resposta = time.time() - session.get("inicio_pergunta", session["inicio_tempo"])
    resposta_gravada = Jogador.salvar_resposta(
        session["resultado_id"], pergunta_atual.id, resposta_escolhida, acertou, tempo_resposta
    )

    # Clique duplo: o 2º POST chega com o cookie antigo e passa pela checagem acima,
    # mas o banco recusa a resposta repetida. Não soma nada de novo.
    if not resposta_gravada:
        ressincronizar_session(perguntas, indice)
        return redirect(url_for("pergunta"))

    session["pontuacao"] += motor.pontuacao
    session["acertos"] += motor.acertos
    session["pergunta_atual"] += 1

    # Ferramenta de estudo: quem errou vê qual era a alternativa certa
    letras = ["a", "b", "c", "d"]
    alternativas_por_letra = dict(zip(letras, pergunta_atual.alternativas))
    letra_correta = pergunta_atual.resposta_correta

    return render_template(
        "comentario.html",
        acertou=acertou,
        comentario=comentario,
        letra_correta=letra_correta,
        texto_correto=alternativas_por_letra.get(letra_correta, ""),
        pontuacao=session["pontuacao"],
        acertos=session["acertos"],
    )


# Chamada quando a pergunta atual já tinha resposta no banco (clique duplo). O cookie
# que o navegador guardar por último pode ser o do 2º POST, com o estado de antes da
# resposta; se a session só "não avançasse", a pessoa ficaria presa nessa pergunta
# (toda resposta seria recusada). O banco é a fonte da verdade: refaz pontuação e
# acertos a partir das respostas gravadas e passa para a próxima pergunta.
def ressincronizar_session(perguntas, indice):
    perguntas_por_id = {pergunta.id: pergunta for pergunta in perguntas}
    motor = MotorQuiz(Jogador(session["nome"]), perguntas)

    for pergunta_id, resposta_dada in Jogador.buscar_respostas_da_partida(session["resultado_id"]):
        if pergunta_id in perguntas_por_id:
            motor.verificar_resposta(perguntas_por_id[pergunta_id], resposta_dada)

    session["pontuacao"] = motor.pontuacao
    session["acertos"] = motor.acertos
    session["pergunta_atual"] = indice + 1
