from database.iniciar_banco import gerar_banco
from classes.class_jogador import Jogador
from classes.class_pergunta import Pergunta
from servicos.motor_quiz import MotorQuiz

gerar_banco()

perguntas = Pergunta.buscar_todas()
jogador = Jogador(input("Digite seu nome: "))

motor = MotorQuiz(jogador, perguntas)
pontuacao, acertos, tempo = motor.jogar()

print(f"\nFim de jogo! Pontuação: {pontuacao} | Acertos: {acertos} | Tempo: {tempo:.2f}s")