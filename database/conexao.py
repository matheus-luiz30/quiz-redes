import os
import sqlite3

# Caminho absoluto do banco, calculado a partir desta pasta: funciona mesmo se o
# gunicorn (ou um script) for iniciado de outra pasta. Com "banco.db" relativo, o
# SQLite criaria um banco novo e vazio em outro lugar, sem avisar.
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_BANCO = os.path.join(PASTA_PROJETO, "banco.db")

# Segundos que uma conexão espera se outra estiver gravando, antes de desistir com
# "database is locked". Cada gravação do quiz leva milissegundos; 15s é folga larga
# para o pico do evento (padrão do Python: 5s).
TEMPO_ESPERA_BANCO = 15


def conectar():
    return sqlite3.connect(CAMINHO_BANCO, timeout=TEMPO_ESPERA_BANCO)
