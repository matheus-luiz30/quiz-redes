# Quiz Redes

Quiz interativo sobre redes de computadores e tecnologia, com um host que comenta as respostas com humor (usando trocadilhos de TI) e gera um perfil do jogador ao final.

Desenvolvido como parte de projeto de bolsa de pesquisa na UFSM, com submissão prevista para a JAE 2026.

## Funcionalidades

- Quiz com perguntas de dificuldade acessível sobre redes/tecnologia
- Host com personalidade que comenta acertos e erros
- Geração de perfil do jogador ao final (ex: "Administrador de Redes | Modo Rápido | 90% de acerto")
- Leaderboard salvo em SQLite

## Como rodar

\`\`\`
python main.py
\`\`\`

## Tecnologias

- Python
- SQLite

## Estrutura do projeto

- `classes/` — classes Jogador e Pergunta
- `database/` — criação e estrutura do banco
- `reutilizavel/` — funções de validação
- `servicos/` — motor do quiz