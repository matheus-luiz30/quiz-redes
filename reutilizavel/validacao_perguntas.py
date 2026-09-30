# Lógica pura do cadastro em lote: recebe uma linha do CSV (dicionário) e devolve
# a lista de erros encontrados. Não lê arquivo nem toca no banco.

COLUNAS_CSV = ["enunciado", "a", "b", "c", "d", "correta", "categoria", "dificuldade"]
DIFICULDADES = ["facil", "medio", "dificil"]


def linha_esta_vazia(linha):
    # O Excel costuma deixar linhas só com ";;;;;;;" no fim do arquivo
    return all((valor or "").strip() == "" for valor in linha.values())


def normalizar_enunciado(enunciado):
    return " ".join(enunciado.split()).lower()


def validar_linha_pergunta(linha, enunciados_ja_vistos):
    erros = []

    for coluna in ["enunciado", "a", "b", "c", "d", "categoria"]:
        if (linha.get(coluna) or "").strip() == "":
            erros.append(f"coluna '{coluna}' vazia")

    correta = (linha.get("correta") or "").strip().lower()
    if correta not in ["a", "b", "c", "d"]:
        erros.append(f"'correta' deve ser a, b, c ou d (veio '{correta}')")

    dificuldade = (linha.get("dificuldade") or "").strip().lower()
    if dificuldade != "" and dificuldade not in DIFICULDADES:
        erros.append(f"'dificuldade' deve ser facil, medio ou dificil (veio '{dificuldade}')")

    enunciado = normalizar_enunciado(linha.get("enunciado") or "")
    if enunciado != "" and enunciado in enunciados_ja_vistos:
        erros.append("enunciado repetido (no CSV ou já cadastrado no banco)")

    return erros
