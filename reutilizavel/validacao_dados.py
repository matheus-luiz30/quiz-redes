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
    "estudante_ufsm": "Estudante UFSM",
    "estudante_outra": "Estudante de outra instituição",
    "profissional": "Profissional da área",
    "outro": "Outro",
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
