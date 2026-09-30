# Exporta os dados do modo web para análise no Excel / Python.
#
# Uso (na pasta do projeto):
#   python exportar_dados.py
#
# Gera em exportacoes/ dois arquivos CSV (";" e UTF-8 com BOM, abrem direto no Excel pt-BR):
#   respostas_AAAA-MM-DD_HH-MM-SS.csv  -> uma linha por resposta dada
#   partidas_AAAA-MM-DD_HH-MM-SS.csv   -> uma linha por partida
#
# No Python: pandas.read_csv(arquivo, sep=";", decimal=",", encoding="utf-8-sig")
import csv
import os
from datetime import datetime

from classes.class_relatorio import Relatorio
from database.conexao import CAMINHO_BANCO, PASTA_PROJETO
from reutilizavel.formatacao_csv import formatar_linha

PASTA_EXPORTACOES = os.path.join(PASTA_PROJETO, "exportacoes")


def salvar_csv(nome_base, carimbo, colunas, linhas):
    caminho = os.path.join(PASTA_EXPORTACOES, f"{nome_base}_{carimbo}.csv")

    with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(colunas)
        for linha in linhas:
            escritor.writerow(formatar_linha(linha))

    print(f"{caminho}: {len(linhas)} linhas")


def main():
    if not os.path.exists(CAMINHO_BANCO):
        print(f"Banco não encontrado em {CAMINHO_BANCO}")
        return

    os.makedirs(PASTA_EXPORTACOES, exist_ok=True)
    carimbo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    colunas, linhas = Relatorio.buscar_respostas()
    salvar_csv("respostas", carimbo, colunas, linhas)

    colunas, linhas = Relatorio.buscar_partidas()
    salvar_csv("partidas", carimbo, colunas, linhas)


if __name__ == "__main__":
    main()
