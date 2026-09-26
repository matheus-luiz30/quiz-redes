# Quiz Redes

Quiz de perguntas e respostas sobre Redes de Computadores, pensado como **ferramenta de
estudo**. Um host com personalidade comenta cada resposta com humor/trocadilhos de rede, e
ao final o sistema gera um perfil do jogador (ex: "Administrador de Redes | Modo Rápido")
a partir da taxa de acerto e do tempo médio por pergunta. Há também um ranking com as
melhores partidas.

Projeto de bolsa de pesquisa na UFSM (programa FIEN-UFSM), com resumo aceito na 41ª
Jornada Acadêmica Integrada (JAI-UFSM, novembro de 2026).

## Funcionalidades

- Quiz com perguntas de múltipla escolha sobre redes de computadores
- Host que comenta acertos e erros com humor
- Perfil do jogador ao final, calculado a partir de acertos e tempo
- Ranking (top 10) com as melhores partidas já jogadas
- Dois modos de uso: terminal e web (mesma lógica e mesmo banco de dados)

## Tecnologias

- Python
- SQLite
- Flask + Jinja2 (modo web, renderização no servidor, sem JavaScript e sem API/JSON)

## Como instalar (Windows)

Criar e ativar o ambiente virtual:

```
python -m venv venv
.\venv\bin\Activate.ps1
pip install flask
```

## Como rodar

Modo web (recomendado):

```
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador.

Modo terminal:

```
python main.py
```

Em ambos os modos o banco `banco.db` é criado automaticamente na primeira execução.

## Cadastrando perguntas

Ainda não há um modo de cadastro em lote. Para adicionar uma pergunta, edite os dados em
`adicionar_perguntas.py` e rode:

```
python adicionar_perguntas.py
```

## Estrutura do projeto

```
quiz-redes/
├── classes/
│   ├── class_jogador.py       # classe Jogador (salvar_no_banco, salvar_resultado, obter_totais, obter_ranking)
│   └── class_pergunta.py      # classe Pergunta (salvar_no_banco, buscar_todas)
├── database/
│   └── gerar_banco.py         # cria as tabelas jogadores, resultados e perguntas (com FKs)
├── reutilizavel/
│   ├── validacao_dados.py     # validar_nome, validar_resposta (terminal) e nome_e_valido (web)
│   └── perfil_jogador.py      # calcular_perfil: lógica pura do perfil final do jogador
├── servicos/
│   └── motor_quiz.py          # classe MotorQuiz: verificar_resposta, comentar_host, jogar (terminal)
├── templates/                 # HTMLs do modo web (Jinja2)
│   ├── base.html              # layout comum, com {% block %} reaproveitado pelas outras telas
│   ├── nome.html
│   ├── pergunta.html
│   ├── comentario.html
│   ├── resultado.html
│   └── ranking.html
├── static/
│   └── style.css              # estilo único do modo web
├── adicionar_perguntas.py     # cadastra uma pergunta por vez
├── app.py                     # entrada do modo web (cria o Flask app e chama app.run())
├── views.py                   # rotas do modo web (@app.route)
├── main.py                    # entrada do modo terminal
├── banco.db                   # SQLite (ignorado no git)
└── .gitignore
```

## Ambiente de desenvolvimento

- Windows, PowerShell
- Ambiente virtual em `venv/`, ativado com `.\venv\bin\Activate.ps1`
- Flask 3.1.3
