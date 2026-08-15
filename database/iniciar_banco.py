import sqlite3

def gerar_banco():

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jogadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogador_id INTEGER NOT NULL,
        pontuacao INTEGER NOT NULL,
        acertos INTEGER NOT NULL,
        tempo_total REAL,
        data_partida DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
    )
    """)

    conexao.commit()
    conexao.close()