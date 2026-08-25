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
                SELECT id FROM jogadores WHERE nome = ?
            """, (self.nome,))
            jogador_existente = cursor.fetchone()

            if jogador_existente:
                print("Jogador já cadastrado, reaproveitando registro existente!")
                return jogador_existente[0]

            cursor.execute("""
                INSERT INTO jogadores (nome)
                VALUES (?)
            """, (self.nome,))

            conexao.commit()
            id_gerado = cursor.lastrowid
            print("Jogador cadastrado com sucesso!")
            return id_gerado

        except sqlite3.IntegrityError as erro: # Erro de repetição 'IntegrityError' do sqlite
            print(f"Erro ao cadastrar jogador\n {erro}")

        except Exception as erro:
            print(f"Ocorreu um erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def obter_totais(jogador_id):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(pontuacao), 0), COALESCE(SUM(acertos), 0)
                FROM resultados
                WHERE jogador_id = ?
            """, (jogador_id,))

            return cursor.fetchone()

        except Exception as erro:
            print(f"Erro inesperado: {erro}")
            return (0, 0)

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