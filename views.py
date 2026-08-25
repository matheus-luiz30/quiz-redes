import time

from flask import render_template, request, session, redirect, url_for

from app import app
from classes.class_jogador import Jogador
from classes.class_pergunta import Pergunta
from reutilizavel.validacao_dados import nome_e_valido
from reutilizavel.perfil_jogador import calcular_perfil
from servicos.motor_quiz import MotorQuiz


@app.route("/")
def index():
    return render_template("nome.html")


@app.route("/comecar", methods=["POST"])
def comecar():
    nome = request.form["nome"].strip()

    if not nome_e_valido(nome):
        return render_template(
            "nome.html",
            erro="Nome inválido: use só letras, entre 3 e 20 caracteres.",
        )

    jogador = Jogador(nome)
    jogador_id = jogador.salvar_no_banco()

    session["jogador_id"] = jogador_id
    session["nome"] = nome
    session["pergunta_atual"] = 0
    session["pontuacao"] = 0
    session["acertos"] = 0
    session["inicio_tempo"] = time.time()
    session["resultado_salvo"] = False

    return redirect(url_for("pergunta"))


@app.route("/pergunta")
def pergunta():
    perguntas = Pergunta.buscar_todas()
    indice = session["pergunta_atual"]

    if indice >= len(perguntas):
        if not session["resultado_salvo"]:
            session["tempo_total"] = time.time() - session["inicio_tempo"]
            Jogador.salvar_resultado(
                session["jogador_id"], session["pontuacao"], session["acertos"], session["tempo_total"]
            )
            session["resultado_salvo"] = True

        total_pontuacao, total_acertos = Jogador.obter_totais(session["jogador_id"])
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
            total_pontuacao=total_pontuacao,
            total_acertos=total_acertos,
        )

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
    resposta_escolhida = request.form["resposta"]

    perguntas = Pergunta.buscar_todas()
    indice = session["pergunta_atual"]
    pergunta_atual = perguntas[indice]

    jogador = Jogador(session["nome"])
    motor = MotorQuiz(jogador, [pergunta_atual])

    acertou = motor.verificar_resposta(pergunta_atual, resposta_escolhida)
    comentario = motor.comentar_host(acertou)

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
