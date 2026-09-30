# Configuração do gunicorn (servidor de produção). Uso, na pasta do projeto:
#   gunicorn app:app
# (o gunicorn lê este arquivo automaticamente)

# Só escuta localmente; o acesso de fora passa pelo proxy (nginx), a definir na etapa 7
bind = "127.0.0.1:8000"

# Processos atendendo em paralelo. SQLite em WAL + timeout aguenta bem poucos workers;
# mais que isso só aumenta a disputa pela gravação no banco.
workers = 3

# Carrega o app uma vez antes de criar os workers: gerar_banco() roda uma única vez,
# em vez de os 3 workers tentarem criar tabelas/colunas ao mesmo tempo.
preload_app = True

timeout = 30
accesslog = "-"
errorlog = "-"
