# Fica em reutilizavel/ (e não como método de Jogador) porque é lógica pura:
# só recebe números e devolve texto, sem tocar no banco. Jogador mistura só
# métodos que fazem I/O (sqlite3, try/except/finally); separar evita acoplar
# regra de negócio a acesso a dados.
def calcular_perfil(acertos, total_perguntas, tempo_total):
    if total_perguntas == 0:
        return ("Sem perguntas respondidas", "Modo Indefinido")

    percentual_acerto = (acertos / total_perguntas) * 100

    if percentual_acerto >= 90:
        titulo = "Administrador de Redes"
    elif percentual_acerto >= 70:
        titulo = "Técnico de Redes Pleno"
    elif percentual_acerto >= 50:
        titulo = "Estagiário de TI"
    else:
        titulo = "Reiniciando o Roteador"

    tempo_medio = tempo_total / total_perguntas

    if tempo_medio <= 10:
        modo = "Modo Rápido"
    else:
        modo = "Modo Tranquilo"

    return (titulo, modo)
