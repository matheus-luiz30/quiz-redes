# Lógica pura da exportação: converte cada valor para o texto que o Excel em
# pt-BR entende. Não lê o banco nem escreve arquivo.


def formatar_celula(valor):
    if valor is None:
        return ""

    # Excel pt-BR usa vírgula como separador decimal: 3.5 viraria texto ou data
    if isinstance(valor, float):
        return f"{valor:.3f}".replace(".", ",")

    return str(valor)


def formatar_linha(linha):
    return [formatar_celula(valor) for valor in linha]
