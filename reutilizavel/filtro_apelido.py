import re
import unicodedata

# Filtro simples de apelidos ofensivos (lógica pura, sem banco). Não é perfeito:
# o objetivo é barrar o óbvio no ranking público do evento. Para incluir palavras,
# acrescente na lista certa (sem acento, minúsculas).

# Só contam como palavra inteira, porque aparecem dentro de palavras normais:
# "puta" em "computacao", "cu" em "curioso", "bicha" em "bichano".
PALAVRAS_INTEIRAS = [
    "cu", "puta", "puto", "foda", "xota", "bicha", "corno", "nazi", "fdp", "pqp", "vsf",
    "vtnc", "tnc", "fuck", "shit", "dick",
]

# Contam mesmo no meio do apelido ("seucaralho", "xxporraxx").
PEDACOS_OFENSIVOS = [
    # palavrões
    "porra", "caralho", "merda", "bosta", "cacete", "fodase", "foder", "fuder", "putaria",
    "buceta", "boceta", "xoxota", "piroca", "punheta", "siririca", "cuzao", "arrombad",
    "vagabund", "otario", "babaca", "imbecil",
    # discriminação / violência
    "viado", "viadao", "sapatao", "traveco", "retardad", "mongoloide", "nazista", "hitler",
    "estupr", "pedofil",
    # inglês
    "fucker", "fucking", "bitch", "pussy", "nigger", "nigga",
]

# Troca números/símbolos comuns por letras: "p0rr4" -> "porra"
TROCAS_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})


def _normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = texto.translate(TROCAS_LEET)
    # Letras repetidas viram uma só: "poooorra" -> "pora" (a lista passa pelo mesmo processo)
    return re.sub(r"(.)\1+", r"\1", texto)


INTEIRAS_NORMALIZADAS = {_normalizar(palavra) for palavra in PALAVRAS_INTEIRAS}
PEDACOS_NORMALIZADOS = [_normalizar(palavra) for palavra in PEDACOS_OFENSIVOS]


def apelido_e_ofensivo(apelido):
    texto = _normalizar(apelido)
    palavras_do_apelido = re.findall(r"[a-z]+", texto)
    # "p.u.t.a" ou "p u t a" viram "puta" quando juntamos tudo
    tudo_junto = "".join(palavras_do_apelido)
    candidatos = set(palavras_do_apelido) | {tudo_junto}
    # plural simples: "corno" também pega "cornos"
    candidatos |= {palavra[:-1] for palavra in candidatos if palavra.endswith("s")}

    if candidatos & INTEIRAS_NORMALIZADAS:
        return True

    for pedaco in PEDACOS_NORMALIZADOS:
        if pedaco in tudo_junto:
            return True

    return False
