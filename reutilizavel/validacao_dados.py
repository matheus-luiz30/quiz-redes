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