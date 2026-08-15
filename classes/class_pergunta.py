import sqlite3

class Pergunta:
    def __init__(self, enunciado, alternativas, resposta_correta, categoria=None, dificuldade="medio"):
        self.enunciado = enunciado
        self.alternativas = alternativas  # lista: ["Ethernet", "Wi-Fi", "Fibra Óptica", "Bluetooth"]
        self.resposta_correta = resposta_correta
        self.categoria = categoria
        self.dificuldade = dificuldade

    def salvar_no_banco(self):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO perguntas 
                (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta, categoria, dificuldade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.enunciado, self.alternativas[0], self.alternativas[1],
                  self.alternativas[2], self.alternativas[3], self.resposta_correta,
                  self.categoria, self.dificuldade))

            conexao.commit()
            print("Pergunta cadastrada com sucesso!")

        except Exception as erro:
            print(f"Ocorreu um erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def buscar_todas():
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM perguntas")
            linhas = cursor.fetchall()

            perguntas = []
            for linha in linhas:
                pergunta = Pergunta(
                    enunciado=linha[1],
                    alternativas=[linha[2], linha[3], linha[4], linha[5]],
                    resposta_correta=linha[6],
                    categoria=linha[7],
                    dificuldade=linha[8]
                )
                perguntas.append(pergunta)

            return perguntas

        except Exception as erro:
            print(f"Ocorreu um erro inesperado: {erro}")
            return []

        finally:
            if conexao:
                conexao.close()