from classes.class_pergunta import Pergunta

pergunta = Pergunta(
    enunciado="O que significa a sigla DNS?",
    alternativas=["Domain Name System", "Data Network Service", "Digital Node Server", "Direct Network Switch"],
    resposta_correta="a",
    categoria="Redes",
    dificuldade="facil"
)

pergunta.salvar_no_banco()