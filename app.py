import os
from datetime import timedelta

import __main__
from flask import Flask

from database.gerar_banco import gerar_banco

app = Flask(__name__)

# True quando iniciado com "python app.py" (desenvolvimento). Não dá para usar só
# __name__ == "__main__": o views.py importa este arquivo de novo como módulo "app".
EXECUTANDO_DIRETO = os.path.abspath(getattr(__main__, "__file__", "")) == os.path.abspath(__file__)

# A chave que assina o cookie da session vem de variável de ambiente, nunca do
# código (quem tem a chave consegue forjar sessions). No servidor ela é obrigatória.
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    if EXECUTANDO_DIRETO:
        app.secret_key = "chave-so-para-desenvolvimento-local"
    else:
        raise RuntimeError(
            "Variável de ambiente SECRET_KEY não definida. Gere uma com:\n"
            '  python -c "import secrets; print(secrets.token_hex(32))"'
        )

# Session dura alguns dias (em vez de acabar ao fechar o navegador), para a
# origem e o número da tentativa não se perderem entre uma partida e outra.
app.permanent_session_lifetime = timedelta(days=7)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

gerar_banco()

from views import *

# "python app.py" = só para desenvolvimento no seu computador (debug ligado,
# acessível só em 127.0.0.1). No servidor quem sobe o app é o gunicorn, que não
# executa este bloco — lá o debug fica sempre desligado.
if __name__ == "__main__":
    app.run(debug=True)
