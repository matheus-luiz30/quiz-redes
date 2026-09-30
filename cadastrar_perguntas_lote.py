# Cadastro de perguntas em lote a partir de um CSV (separador ";", salvo como
# "CSV UTF-8" no Excel). Colunas: enunciado;a;b;c;d;correta;categoria;dificuldade
#
# Uso:
#   python cadastrar_perguntas_lote.py perguntas.csv             -> valida e grava
#   python cadastrar_perguntas_lote.py perguntas.csv --simular   -> só valida, não grava
#
# Se qualquer linha tiver erro, nenhuma pergunta é gravada.
import csv
import sys

from classes.class_pergunta import Pergunta
from database.gerar_banco import gerar_banco
from reutilizavel.validacao_perguntas import (
    COLUNAS_CSV, linha_esta_vazia, normalizar_enunciado, validar_linha_pergunta,
)


def ler_csv(caminho):
    # utf-8-sig: aceita o BOM que o Excel coloca no início do "CSV UTF-8"
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        cabecalho = [coluna.strip().lower() for coluna in (leitor.fieldnames or [])]
        linhas = list(leitor)
    return cabecalho, linhas


def main():
    if len(sys.argv) < 2:
        print("Uso: python cadastrar_perguntas_lote.py arquivo.csv [--simular]")
        return

    caminho = sys.argv[1]
    simular = "--simular" in sys.argv

    try:
        cabecalho, linhas = ler_csv(caminho)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        return
    except UnicodeDecodeError:
        print("Erro de codificação: salve o arquivo como 'CSV UTF-8 (delimitado por vírgulas)' no Excel.")
        return

    if cabecalho != COLUNAS_CSV:
        print("Cabeçalho inválido.")
        print(f"  Esperado: {';'.join(COLUNAS_CSV)}")
        print(f"  Veio:     {';'.join(cabecalho)}")
        return

    gerar_banco()  # garante que a tabela perguntas existe (não apaga nada)
    enunciados_ja_vistos = {normalizar_enunciado(p.enunciado) for p in Pergunta.buscar_todas()}

    perguntas = []
    erros_por_linha = []

    # numero_linha começa em 2 porque a linha 1 do arquivo é o cabeçalho
    for numero_linha, linha in enumerate(linhas, start=2):
        linha = {chave.strip().lower(): valor for chave, valor in linha.items() if chave is not None}

        if linha_esta_vazia(linha):
            continue

        erros = validar_linha_pergunta(linha, enunciados_ja_vistos)
        if erros:
            erros_por_linha.append((numero_linha, erros))
            continue

        enunciados_ja_vistos.add(normalizar_enunciado(linha["enunciado"]))
        perguntas.append(Pergunta(
            enunciado=linha["enunciado"].strip(),
            alternativas=[linha["a"].strip(), linha["b"].strip(), linha["c"].strip(), linha["d"].strip()],
            resposta_correta=linha["correta"].strip().lower(),
            categoria=linha["categoria"].strip(),
            dificuldade=(linha["dificuldade"] or "").strip().lower() or "medio",
        ))

    if erros_por_linha:
        print(f"{len(erros_por_linha)} linha(s) com erro — nada foi gravado:")
        for numero_linha, erros in erros_por_linha:
            print(f"  Linha {numero_linha}: {'; '.join(erros)}")
        return

    if not perguntas:
        print("Nenhuma pergunta encontrada no arquivo.")
        return

    if simular:
        print(f"Simulação: {len(perguntas)} perguntas válidas. Nada foi gravado.")
        return

    Pergunta.salvar_varias_no_banco(perguntas)


if __name__ == "__main__":
    main()
