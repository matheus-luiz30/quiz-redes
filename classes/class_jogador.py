import sqlite3

class Jogador:
    def __init__(self, nome):
        self.nome = nome

    def salvar_no_banco(self):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO jogadores (nome)
                VALUES (?)
            """, (self.nome,))

            conexao.commit()
            id_gerado = cursor.lastrowid  # pega o id que o AUTOINCREMENT acabou de criar
            print("Jogador cadastrado com sucesso!")
            return id_gerado

        except sqlite3.IntegrityError as erro:
            print(f"Erro ao cadastrar jogador\n {erro}")

        except Exception as erro:
            print(f"Ocorreu um erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def salvar_resultado(jogador_id, pontuacao, acertos, tempo_total):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO resultados (jogador_id, pontuacao, acertos, tempo_total)
                VALUES (?, ?, ?, ?)
            """, (jogador_id, pontuacao, acertos, tempo_total))

            conexao.commit()
            print("Resultado salvo com sucesso!")

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()