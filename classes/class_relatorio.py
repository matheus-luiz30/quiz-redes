from database.conexao import conectar

# Consultas usadas na exportação para análise estatística. Regras comuns:
# - só partidas do modo web (origem NULL = modo terminal ou teste antigo, fica de fora)
# - o apelido não é exportado (desnecessário para a análise)
# - data_partida convertida de UTC (CURRENT_TIMESTAMP do SQLite) para horário de Brasília
# - partida finalizada = tempo_total preenchido (ver Jogador.iniciar_resultado)


class Relatorio:

    @staticmethod
    def _executar(consulta):
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute(consulta)
            linhas = cursor.fetchall()
            colunas = [descricao[0] for descricao in cursor.description]
            return colunas, linhas

        except Exception as erro:
            print(f"Erro inesperado: {erro}")
            return [], []

        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def buscar_respostas():
        return Relatorio._executar("""
            SELECT resultados.id AS resultado_id,
                   datetime(resultados.data_partida, '-3 hours') AS data_partida,
                   jogadores.vinculo,
                   resultados.origem,
                   resultados.tentativa,
                   CASE WHEN resultados.tempo_total IS NOT NULL THEN 'sim' ELSE 'não' END AS partida_finalizada,
                   resultado_perguntas.pergunta_id,
                   perguntas.enunciado,
                   perguntas.categoria,
                   perguntas.dificuldade,
                   resultado_perguntas.acertou,
                   resultado_perguntas.tempo_resposta
            FROM resultado_perguntas
            JOIN resultados ON resultados.id = resultado_perguntas.resultado_id
            JOIN jogadores ON jogadores.id = resultados.jogador_id
            LEFT JOIN perguntas ON perguntas.id = resultado_perguntas.pergunta_id
            WHERE resultados.origem IS NOT NULL
            ORDER BY resultados.id, resultado_perguntas.id
        """)

    @staticmethod
    def buscar_partidas():
        return Relatorio._executar("""
            SELECT resultados.id AS resultado_id,
                   datetime(resultados.data_partida, '-3 hours') AS data_partida,
                   jogadores.vinculo,
                   resultados.origem,
                   resultados.tentativa,
                   CASE WHEN resultados.tempo_total IS NOT NULL THEN 'sim' ELSE 'não' END AS finalizada,
                   resultados.pontuacao,
                   resultados.acertos,
                   resultados.tempo_total
            FROM resultados
            JOIN jogadores ON jogadores.id = resultados.jogador_id
            WHERE resultados.origem IS NOT NULL
            ORDER BY resultados.id
        """)
