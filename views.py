import time

from flask import render_template, request, session, redirect, url_for

from app import app
from classes.class_jogador import Jogador
from classes.class_pergunta import Pergunta
from reutilizavel.validacao_dados import (
    VINCULOS, apelido_e_valido, vinculo_e_valido, gerar_apelido_padrao, normalizar_origem,
)
from reutilizavel.perfil_jogador import calcular_perfil
from reutilizavel.filtro_apelido import apelido_e_ofensivo
from servicos.motor_quiz import MotorQuiz


@app.route("/")
def index():
    # A origem fica na session (e não só na URL) para sobreviver a um clique no
    # logo, a um erro no formulário e ao "Jogar de novo".
    if "origem" in request.args:
        session["origem"] = normalizar_origem(request.args["origem"])

    return render_template("nome.html", vinculos=VINCULOS)


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
    session["origem"] = origem
    session["tentativa"] = tentativa
    return redirect(url_for("index"))


@app.route("/comecar", methods=["POST"])
def comecar():
    apelido = request.form.get("apelido", "").strip()
    vinculo = request.form.get("vinculo", "")

    if not apelido_e_valido(apelido):
        return render_template(
            "nome.html",
            vinculos=VINCULOS,
            apelido=apelido,
            vinculo=vinculo,
            erro="Apelido inválido: use de 2 a 20 letras, números, espaço, _ - ou ponto.",
        )

    if not vinculo_e_valido(vinculo):
        return render_template(
            "nome.html",
            vinculos=VINCULOS,
            apelido=apelido,
            vinculo=vinculo,
            erro="Escolha o seu vínculo para começar.",
        )

    # Apelido ofensivo não gera erro na tela: troca em silêncio pelo padrão
    if apelido == "" or apelido_e_ofensivo(apelido):
        apelido = gerar_apelido_padrao()

    nome = apelido
    jogador = Jogador(nome, vinculo)
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

    resposta_escolhida = request.form["resposta"]

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
    Jogador.salvar_resposta(session["resultado_id"], pergunta_atual.id, acertou, tempo_resposta)

    session["pontuacao"] += motor.pontuacao
    session["acertos"] += motor.acertos
    session["pergunta_atual"] += 1

    return render_template(
        "comentario.html",
        acertou=acertou,
        comentario=comentario,
        pontuacao=session["pontuacao"],
        acertos=session["acertos"],
    )
