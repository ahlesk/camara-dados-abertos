"""4. Analisa os discursos de um deputado em um período determinado, contando a
frequência das palavras (sem stop words), em ordem decrescente.

Exemplo de uso:
    python3 4_analise_discursos.py "Tabata Amaral" 2023-01-01 2026-08-14
"""

import re
import sys

from camara_api import buscar_deputado_por_nome, get_paginado

STOPWORDS_PT = {
    "a", "à", "às", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo",
    "as", "até", "com", "como", "da", "das", "de", "dela", "delas", "dele", "deles",
    "depois", "do", "dos", "e", "é", "ela", "elas", "ele", "eles", "em", "entre",
    "era", "eram", "essa", "essas", "esse", "esses", "esta", "está", "estamos",
    "estão", "estas", "estava", "estavam", "este", "esteja", "estejam", "estes",
    "esteve", "estive", "estivemos", "estiveram", "estou", "eu", "foi", "fomos",
    "for", "foram", "fosse", "fossem", "fui", "há", "isso", "isto", "já", "lhe",
    "lhes", "mais", "mas", "me", "mesmo", "meu", "meus", "minha", "minhas", "muito",
    "na", "nas", "não", "nem", "no", "nos", "nós", "nossa", "nossas", "nosso",
    "nossos", "num", "numa", "o", "os", "ou", "para", "pela", "pelas", "pelo",
    "pelos", "por", "qual", "quando", "que", "quem", "se", "seja", "sejam", "sem",
    "ser", "será", "serão", "seu", "seus", "só", "somos", "sua", "suas", "também",
    "te", "tem", "tém", "temos", "tenha", "tenham", "tenho", "ter", "teu", "teus",
    "teve", "tinha", "tinham", "tive", "tivemos", "tiveram", "tu", "tua", "tuas",
    "um", "uma", "umas", "uns", "você", "vocês", "vos", "sr", "sra", "srs", "deputado",
    "deputada", "presidente", "então", "assim", "aqui", "ali", "onde", "vai", "vou",
    "hoje", "ainda", "cada", "todo", "toda", "todos", "todas", "outro", "outra",
    "outros", "outras", "pode", "podem", "porque", "sobre",
}


def carregar_stopwords():
    """Tenta usar a lista de stopwords do NLTK; se indisponível, usa a lista embutida."""
    try:
        import nltk
        from nltk.corpus import stopwords

        try:
            return set(stopwords.words("portuguese"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("portuguese"))
    except Exception:
        return STOPWORDS_PT


def tokenizar(texto):
    """Extrai palavras do texto, ignorando pontuação e números."""
    return re.findall(r"[a-zà-ú]+", texto.lower())


def buscar_discursos(id_deputado, data_inicio, data_fim):
    return get_paginado(
        f"/deputados/{id_deputado}/discursos",
        {"dataInicio": data_inicio, "dataFim": data_fim},
    )


def contar_palavras(discursos, stopwords_ativas):
    frequencia = {}
    for discurso in discursos:
        texto = discurso.get("transcricao") or discurso.get("sumario") or ""
        for palavra in tokenizar(texto):
            if palavra in stopwords_ativas or len(palavra) < 3:
                continue
            frequencia[palavra] = frequencia.get(palavra, 0) + 1
    return frequencia


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "Tabata Amaral"
    data_inicio = sys.argv[2] if len(sys.argv) > 2 else "2023-01-01"
    data_fim = sys.argv[3] if len(sys.argv) > 3 else "2026-08-14"
    top_n = int(sys.argv[4]) if len(sys.argv) > 4 else 30

    deputado = buscar_deputado_por_nome(nome)
    discursos = buscar_discursos(deputado["id"], data_inicio, data_fim)

    stopwords_ativas = carregar_stopwords()
    frequencia = contar_palavras(discursos, stopwords_ativas)

    ranking = sorted(frequencia, key=lambda p: frequencia[p], reverse=True)

    print(f"Deputado(a): {deputado['nome']}")
    print(f"Período: {data_inicio} até {data_fim}")
    print(f"Discursos encontrados: {len(discursos)}")
    print(f"Palavras únicas (sem stop words): {len(frequencia)}\n")

    for posicao, palavra in enumerate(ranking[:top_n], start=1):
        print(f"{posicao:>2}. {palavra:<20} {frequencia[palavra]}")


if __name__ == "__main__":
    main()
