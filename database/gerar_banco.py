import sqlite3


# SQLite não tem "ADD COLUMN IF NOT EXISTS": consulta as colunas da tabela e só
# adiciona se faltar. Permite evoluir o banco.db existente sem apagar dados.
def adicionar_coluna_se_faltar(cursor, tabela, coluna, tipo):
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas_existentes = [linha[1] for linha in cursor.fetchall()]

    if coluna not in colunas_existentes:
        cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")


def gerar_banco():

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jogadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        vinculo TEXT
    )
    """)
    adicionar_coluna_se_faltar(cursor, "jogadores", "vinculo", "TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogador_id INTEGER NOT NULL,
        pontuacao INTEGER NOT NULL,
        acertos INTEGER NOT NULL,
        tempo_total REAL,
        data_partida DATETIME DEFAULT CURRENT_TIMESTAMP,
        origem TEXT,
        FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
    )
    """)
    adicionar_coluna_se_faltar(cursor, "resultados", "origem", "TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS perguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enunciado TEXT NOT NULL,
        alternativa_a TEXT NOT NULL,
        alternativa_b TEXT NOT NULL,
        alternativa_c TEXT NOT NULL,
        alternativa_d TEXT NOT NULL,
        resposta_correta TEXT NOT NULL,
        categoria TEXT,
        dificuldade TEXT DEFAULT 'medio'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultado_perguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resultado_id INTEGER NOT NULL,
        pergunta_id INTEGER NOT NULL,
        acertou INTEGER NOT NULL CHECK (acertou IN (0, 1)),
        tempo_resposta REAL,
        FOREIGN KEY (resultado_id) REFERENCES resultados (id),
        FOREIGN KEY (pergunta_id) REFERENCES perguntas (id)
    )
    """)

    conexao.commit()
    conexao.close()