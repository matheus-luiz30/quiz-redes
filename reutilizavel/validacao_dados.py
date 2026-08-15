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