"""1. Lista os deputados de um determinado partido em um estado específico.

Exemplo de uso:
    python3 1_deputados_por_partido_uf.py PL SP
    python3 1_deputados_por_partido_uf.py PT MA
"""

import sys

from camara_api import get_paginado


def listar_deputados(partido, uf):
    return get_paginado("/deputados", {"siglaPartido": partido, "siglaUf": uf})


def main():
    partido = sys.argv[1] if len(sys.argv) > 1 else "PL"
    uf = sys.argv[2] if len(sys.argv) > 2 else "SP"

    deputados = listar_deputados(partido, uf)

    print(f"Deputados do {partido} em {uf}: {len(deputados)}\n")
    for dep in sorted(deputados, key=lambda d: d["nome"]):
        print(f"- {dep['nome']} (id {dep['id']})")


if __name__ == "__main__":
    main()
