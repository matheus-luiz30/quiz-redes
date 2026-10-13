import random


def validar_nome():
    while True:
        nome_digitado = input("Digite seu nome: ").strip()
        nome_limpo = nome_digitado.replace(" ", "")

        if not nome_limpo.isalpha():
            print("Erro: Digite apenas letras (sem números ou símbolos).")
            continue

        if len(nome_digitado) < 3 or len(nome_digitado) > 20:
            print("Erro: O nome deve ter entre 3 e 20 caracteres.")
            continue

        return nome_digitado


def nome_e_valido(nome):
    nome_limpo = nome.replace(" ", "")

    if not nome_limpo.isalpha():
        return False

    if len(nome) < 3 or len(nome) > 20:
        return False

    return True


def validar_resposta():
    while True:
        resposta_digitada = input("\nSua resposta (a/b/c/d): ").strip().lower()

        if resposta_digitada not in ["a", "b", "c", "d"]:
            print("Erro: Digite apenas a, b, c ou d.")
            continue

        return resposta_digitada

# Modo web (público externo): código salvo no banco -> texto mostrado na tela.
# Códigos curtos facilitam a análise estatística depois.
VINCULOS = {
    "estudante_redes_ti": "Estudante de Redes/TI",
    "estudante_outro": "Estudante de outro curso",
    "profissional_ti": "Profissional de TI",
    "outro": "Outro",
}

# menor_18 joga normalmente, mas fica fora dos CSVs da pesquisa (exportar_dados.py)
FAIXAS_ETARIAS = {
    "menor_18": "Menos de 18",
    "18_24": "18–24",
    "25_34": "25–34",
    "35_mais": "35 ou mais",
}


def apelido_e_valido(apelido):
    # Vazio é permitido (o sistema gera um apelido padrão)
    if apelido == "":
        return True

    if len(apelido) < 2 or len(apelido) > 20:
        return False

    for caractere in apelido:
        if not (caractere.isalnum() or caractere in " _-."):
            return False

    return True


def vinculo_e_valido(vinculo):
    return vinculo in VINCULOS


def faixa_etaria_e_valida(faixa_etaria):
    return faixa_etaria in FAIXAS_ETARIAS


# Origem do acesso (?origem=instagram, ?origem=qr_errc...). Aceita qualquer código
# curto em minúsculas, para poder criar canais novos sem mexer no código; sem
# parâmetro ou com valor estranho, conta como "direto".
def normalizar_origem(origem):
    origem = (origem or "").strip().lower()

    if origem == "" or len(origem) > 30:
        return "direto"

    for caractere in origem:
        if not (caractere.isascii() and (caractere.isalnum() or caractere in "_-")):
            return "direto"

    return origem


def gerar_apelido_padrao():
    return f"Jogador {random.randint(100, 999)}"
