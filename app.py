from flask import Flask

from database.gerar_banco import gerar_banco

app = Flask(__name__)
app.secret_key = "chave-secreta-quiz-redes"

gerar_banco()

from views import *

if __name__ == "__main__":
    app.run(debug=True)
