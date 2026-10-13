from database.conexao import conectar

# Consultas usadas na exportação para análise estatística. Regras comuns:
# - só partidas do modo web (origem NULL = modo terminal ou teste antigo, fica de fora)
# - partidas de menores de 18 anos ficam de fora (só contadas, ver contar_excluidos_menores)
# - o apelido não é exportado (desnecessário para a análise)
# - datas convertidas de UTC (CURRENT_TIMESTAMP do SQLite) para horário de Brasília
# - partida finalizada = tempo_total preenchido (ver Jogador.iniciar_resultado)

FAIXA_ETARIA_EXCLUIDA = "menor_18"

# faixa_etaria NULL (partidas de antes da pergunta existir) continua na exportação:
# não dá para saber a idade, e "NULL <> 'menor_18'" sozinho daria falso no SQL.
FILTRO_PARTIDAS_WEB = """
    resultados.origem IS NOT NULL
    AND (jogadores.faixa_etaria IS NULL OR jogadores.faixa_etaria <> ?)
"""


class Relatorio:

    @staticmethod
    def _executar(consulta, parametros=()):
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute(consulta, parametros)
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
        return Relatorio._executar(f"""
            SELECT resultados.id AS resultado_id,
                   datetime(resultados.data_partida, '-3 hours') AS data_partida,
                   jogadores.vinculo,
                   jogadores.faixa_etaria,
                   resultados.origem,
                   resultados.tentativa,
                   CASE WHEN resultados.tempo_total IS NOT NULL THEN 'sim' ELSE 'não' END AS partida_finalizada,
                   resultado_perguntas.pergunta_id,
                   perguntas.enunciado,
                   perguntas.categoria,
                   perguntas.dificuldade,
                   resultado_perguntas.resposta_dada,
                   resultado_perguntas.acertou,
                   resultado_perguntas.tempo_resposta,
                   datetime(resultado_perguntas.data_hora, '-3 hours') AS data_hora
            FROM resultado_perguntas
            JOIN resultados ON resultados.id = resultado_perguntas.resultado_id
            JOIN jogadores ON jogadores.id = resultados.jogador_id
            LEFT JOIN perguntas ON perguntas.id = resultado_perguntas.pergunta_id
            WHERE {FILTRO_PARTIDAS_WEB}
            ORDER BY resultados.id, resultado_perguntas.id
        """, (FAIXA_ETARIA_EXCLUIDA,))

    @staticmethod
    def buscar_partidas():
        return Relatorio._executar(f"""
            SELECT resultados.id AS resultado_id,
                   datetime(resultados.data_partida, '-3 hours') AS data_partida,
                   jogadores.vinculo,
                   jogadores.faixa_etaria,
                   resultados.origem,
                   resultados.tentativa,
                   CASE WHEN resultados.tempo_total IS NOT NULL THEN 'sim' ELSE 'não' END AS finalizada,
                   resultados.pontuacao,
                   resultados.acertos,
                   resultados.tempo_total
            FROM resultados
            JOIN jogadores ON jogadores.id = resultados.jogador_id
            WHERE {FILTRO_PARTIDAS_WEB}
            ORDER BY resultados.id
        """, (FAIXA_ETARIA_EXCLUIDA,))

    @staticmethod
    def contar_excluidos_menores():
        # Devolve (partidas, respostas) de menores de 18 no modo web, só para o
        # aviso no terminal; esses dados não saem do banco.
        colunas, linhas = Relatorio._executar("""
            SELECT COUNT(DISTINCT resultados.id),
                   COUNT(resultado_perguntas.id)
            FROM resultados
            JOIN jogadores ON jogadores.id = resultados.jogador_id
            LEFT JOIN resultado_perguntas ON resultado_perguntas.resultado_id = resultados.id
            WHERE resultados.origem IS NOT NULL
              AND jogadores.faixa_etaria = ?
        """, (FAIXA_ETARIA_EXCLUIDA,))

        if not linhas:
            return None, None
        return linhas[0]
