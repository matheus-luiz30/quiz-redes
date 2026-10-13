# Quiz Redes

Quiz de perguntas e respostas sobre Redes de Computadores, pensado como **ferramenta de
estudo**. Um host com personalidade comenta cada resposta com humor/trocadilhos de rede, e
ao final o sistema gera um perfil do jogador (ex: "Administrador de Redes | Modo Rápido")
a partir da taxa de acerto e do tempo médio por pergunta. Há também um ranking com as
melhores partidas.

Projeto de bolsa de pesquisa na UFSM (FIEN-UFSM).

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

As perguntas são cadastradas em lote a partir de um CSV. O modelo está em
`perguntas_modelo.csv`: separador `;`, salvo no Excel como "CSV UTF-8 (delimitado por
vírgulas)".

```
enunciado;a;b;c;d;correta;categoria;dificuldade
Qual porta padrão o HTTPS usa?;80;21;443;8080;c;Protocolos;medio
```

- `enunciado`, `a`, `b`, `c`, `d` e `categoria` são obrigatórias
- `correta`: `a`, `b`, `c` ou `d`
- `dificuldade`: `facil`, `medio` ou `dificil` (sem acento); vazia vira `medio`
- enunciados repetidos são recusados, tanto dentro do CSV quanto em relação ao banco

Primeiro valide sem gravar, depois grave:

```
python cadastrar_perguntas_lote.py perguntas.csv --simular
python cadastrar_perguntas_lote.py perguntas.csv
```

Se qualquer linha tiver erro, nada é gravado, e o script lista os erros com o número da
linha. O `adicionar_perguntas.py` antigo (uma pergunta por vez, editando o código) foi
mantido, mas o caminho recomendado é o CSV.

## Dados coletados (modo web)

O modo web será aplicado ao público da ERRC 2026, e os dados vão para uma análise
estatística. A participação é voluntária e anônima: **não é pedido nome, e-mail nem
nenhum dado que identifique a pessoa**. O apelido é opcional, aparece só no ranking e
não é exportado.

Por partida:

| Dado | Valores |
|---|---|
| `vinculo` | `estudante_redes_ti`, `estudante_outro`, `profissional_ti`, `outro` |
| `faixa_etaria` | `menor_18`, `18_24`, `25_34`, `35_mais` |
| `origem` | por onde a pessoa chegou: `qr_errc`, `instagram`, `direto`... (parâmetro `?origem=` do link) |
| `tentativa` | 1 na primeira partida daquele navegador, 2 na segunda... |
| `data_partida` | data e hora de início |
| `pontuacao`, `acertos`, `tempo_total` | resultado final (`tempo_total` vazio = partida abandonada) |

Por resposta:

| Dado | Valores |
|---|---|
| `pergunta_id` | qual pergunta (com enunciado, categoria e dificuldade) |
| `resposta_dada` | letra marcada (`a` a `d`) |
| `acertou` | 1 ou 0 |
| `tempo_resposta` | segundos entre a pergunta aparecer e a resposta |
| `data_hora` | data e hora da resposta |

### Regra dos menores de 18

Quem marca "Menos de 18" joga normalmente e aparece no ranking, mas **as partidas e
respostas dessas pessoas não entram nos arquivos exportados**. Os dados ficam só no
banco, e a exportação mostra no terminal quantas partidas e respostas foram deixadas de
fora. Partidas antigas, de antes da pergunta de faixa etária existir, ficam com
`faixa_etaria` vazia e continuam na exportação.

## Exportando os dados para análise

Na pasta do projeto, com o ambiente virtual ativado:

```
python exportar_dados.py
```

São gerados dois arquivos em `exportacoes/`:

- `respostas_AAAA-MM-DD_HH-MM-SS.csv`: uma linha por resposta, com os dados da partida
  repetidos em cada linha
- `partidas_AAAA-MM-DD_HH-MM-SS.csv`: uma linha por partida

Detalhes do formato:

- separador `;`, UTF-8 com BOM e vírgula decimal: abrem direto no Excel em português
- datas no horário de Brasília (UTC−3)
- só partidas do modo web (as do terminal ficam de fora) e sem menores de 18

Para abrir no Python:

```python
import pandas as pd
partidas = pd.read_csv("exportacoes/partidas_....csv", sep=";", decimal=",", encoding="utf-8-sig")
```

Para comparar quem ainda não conhecia as perguntas, filtre `tentativa == 1`.

## Estrutura do projeto

```
quiz-redes/
├── classes/                     # só métodos que acessam o banco
│   ├── class_jogador.py         # Jogador: jogadores, partidas, respostas e ranking
│   ├── class_pergunta.py        # Pergunta: cadastro (um a um e em lote) e busca
│   └── class_relatorio.py       # Relatorio: consultas da exportação
├── database/
│   ├── conexao.py               # conectar(): caminho absoluto do banco.db + timeout
│   └── gerar_banco.py           # cria as tabelas, liga o WAL e adiciona colunas novas
├── reutilizavel/                # lógica pura, sem acesso ao banco
│   ├── validacao_dados.py       # validações do terminal e da tela inicial do web
│   ├── perfil_jogador.py        # calcular_perfil: perfil final do jogador
│   ├── filtro_apelido.py        # bloqueio de apelidos ofensivos
│   ├── validacao_perguntas.py   # regras do CSV de cadastro em lote
│   └── formatacao_csv.py        # números com vírgula decimal para o Excel pt-BR
├── servicos/
│   └── motor_quiz.py            # MotorQuiz: verificar_resposta, comentar_host, jogar (terminal)
├── templates/                   # HTMLs do modo web (Jinja2)
│   ├── base.html                # layout comum, reaproveitado pelas outras telas
│   ├── _tabela_ranking.html     # tabela do top 10 (resultado e ranking)
│   ├── nome.html                # apelido, vínculo, faixa etária e consentimento
│   ├── pergunta.html
│   ├── comentario.html          # comentário do host e resposta certa quando erra
│   ├── resultado.html           # perfil + top 10 com a partida destacada
│   └── ranking.html
├── static/
│   └── style.css                # estilo único, mobile first, sem JavaScript
├── adicionar_perguntas.py       # cadastra uma pergunta por vez (antigo)
├── cadastrar_perguntas_lote.py  # cadastro em lote via CSV
├── perguntas_modelo.csv         # cabeçalho do CSV de cadastro
├── exportar_dados.py            # gera os CSVs para análise em exportacoes/
├── app.py                       # entrada do modo web
├── views.py                     # rotas do modo web
├── main.py                      # entrada do modo terminal
├── gunicorn.conf.py             # configuração de produção (servidor Linux)
├── requirements.txt             # dependências com versões fixas
├── banco.db (+ -wal, -shm)      # SQLite (ignorado no git)
├── exportacoes/                 # saída do exportar_dados.py (ignorada no git)
└── .gitignore
```

## Ambiente de desenvolvimento

- Windows, PowerShell
- Ambiente virtual em `venv/`, ativado com `.\venv\bin\Activate.ps1`
- Flask 3.1.3
