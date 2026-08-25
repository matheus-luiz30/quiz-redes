from classes.class_pergunta import Pergunta

pergunta = Pergunta(
    enunciado="enunciado teste",
    alternativas=["a", "b", "c", "d"],
    resposta_correta="d",
    categoria="teste",
    dificuldade="dificil"
)

pergunta.salvar_no_banco()