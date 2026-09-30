import sqlite3

class Jogador:
    def __init__(self, nome, vinculo=None):
        self.nome = nome
        self.vinculo = vinculo  # só o modo web preenche; terminal grava NULL

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

    # Modo web: sempre cria um jogador novo por partida, porque apelidos se repetem
    # entre pessoas diferentes e cada uma tem seu vínculo. (O terminal continua
    # usando salvar_no_banco, que reaproveita pelo nome.)
    def salvar_novo_no_banco(self):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO jogadores (nome, vinculo)
                VALUES (?, ?)
            """, (self.nome, self.vinculo))

            conexao.commit()
            return cursor.lastrowid

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
    def obter_ranking(limite=10):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT nome, pontuacao, acertos, tempo_total
                FROM (
                    SELECT jogadores.nome, resultados.pontuacao, resultados.acertos, resultados.tempo_total,
                           ROW_NUMBER() OVER (
                               PARTITION BY resultados.jogador_id
                               ORDER BY resultados.pontuacao DESC, resultados.tempo_total ASC, resultados.id ASC
                           ) AS posicao_jogador
                    FROM resultados
                    JOIN jogadores ON jogadores.id = resultados.jogador_id
                    WHERE resultados.tempo_total IS NOT NULL
                )
                WHERE posicao_jogador = 1
                ORDER BY pontuacao DESC, tempo_total ASC
                LIMIT ?
            """, (limite,))

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro inesperado: {erro}")
            return []

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

    # Modo web: a partida é criada no início (pontuacao/acertos zerados, tempo_total NULL)
    # para que cada resposta já tenha um resultado_id ao qual se ligar. No fim do jogo,
    # finalizar_resultado() preenche os valores. tempo_total NULL = partida abandonada.
    @staticmethod
    def iniciar_resultado(jogador_id, origem):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("""
                INSERT INTO resultados (jogador_id, pontuacao, acertos, origem)
                VALUES (?, 0, 0, ?)
            """, (jogador_id, origem))

            conexao.commit()
            return cursor.lastrowid

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def finalizar_resultado(resultado_id, pontuacao, acertos, tempo_total):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE resultados
                SET pontuacao = ?, acertos = ?, tempo_total = ?
                WHERE id = ?
            """, (pontuacao, acertos, tempo_total, resultado_id))

            conexao.commit()
            print("Resultado salvo com sucesso!")

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def salvar_resposta(resultado_id, pergunta_id, acertou, tempo_resposta):
        conexao = None
        try:
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("""
                INSERT INTO resultado_perguntas (resultado_id, pergunta_id, acertou, tempo_resposta)
                VALUES (?, ?, ?, ?)
            """, (resultado_id, pergunta_id, int(acertou), tempo_resposta))

            conexao.commit()

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

        finally:
            if conexao:
                conexao.close()
