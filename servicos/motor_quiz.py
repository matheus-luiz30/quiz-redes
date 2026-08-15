import random
import time
from classes.class_jogador import Jogador
from reutilizavel.validacao_dados import validar_resposta


class MotorQuiz:

    comentarios_acerto = [
        "Isso aí! Sua conexão neural rodou sem lag nenhum.",
        "Resposta certa, sem 404 aqui!",
        "Boa! Você tá com o firewall mental afiado hoje.",
        "Acertou! Isso sim é fibra óptica de raciocínio.",
    ]

    comentarios_erro = [
        "Ops, essa resposta caiu na exceção... tenta de novo na próxima!",
        "Erro 403: acesso à resposta certa negado dessa vez.",
        "Quase! Parece que sua conexão teve um pacote perdido aí.",
        "Não foi dessa vez — recalibra o roteador e bora pra próxima!",
    ]

    def __init__(self, jogador, perguntas):
        self.jogador = jogador
        self.perguntas = perguntas
        self.pontuacao = 0
        self.acertos = 0

    def verificar_resposta(self, pergunta, resposta_jogador):
        acertou = resposta_jogador == pergunta.resposta_correta

        if acertou:
            self.pontuacao += 10
            self.acertos += 1

        return acertou

    def comentar_host(self, acertou):
        if acertou:
            return random.choice(self.comentarios_acerto)
        else:
            return random.choice(self.comentarios_erro)

    def jogar(self):
        inicio = time.time()

        for pergunta in self.perguntas:
            print(f"\n{pergunta.enunciado}")
            letras = ["a", "b", "c", "d"]
            for letra, alternativa in zip(letras, pergunta.alternativas):
                print(f"{letra}) {alternativa}")

            resposta_jogador = validar_resposta()

            acertou = self.verificar_resposta(pergunta, resposta_jogador)
            print(self.comentar_host(acertou))

        tempo_total = time.time() - inicio

        jogador_id = self.jogador.salvar_no_banco()
        Jogador.salvar_resultado(jogador_id, self.pontuacao, self.acertos, tempo_total)

        return self.pontuacao, self.acertos, tempo_total