"""3. Lista os fornecedores que mais receberam recursos da cota parlamentar,
em ordem decrescente de valor.

Exemplo de uso:
    python3 3_maiores_fornecedores.py "Tabata Amaral" 2026
"""

import sys

from camara_api import buscar_deputado_por_nome, get_paginado


def gastos_por_fornecedor(id_deputado, id_legislatura, ano):
    despesas = get_paginado(
        f"/deputados/{id_deputado}/despesas",
        {"ano": ano, "idLegislatura": id_legislatura},
    )

    fornecedores = {}
    for despesa in despesas:
        nome = despesa["nomeFornecedor"]
        fornecedores[nome] = fornecedores.get(nome, 0) + despesa["valorLiquido"]

    return fornecedores


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "Tabata Amaral"
    ano = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    deputado = buscar_deputado_por_nome(nome)
    fornecedores = gastos_por_fornecedor(deputado["id"], deputado["idLegislatura"], ano)

    ranking = sorted(fornecedores, key=lambda f: fornecedores[f], reverse=True)

    print(f"Maiores fornecedores de {deputado['nome']} em {ano}:\n")
    for posicao, fornecedor in enumerate(ranking[:top_n], start=1):
        valor = fornecedores[fornecedor]
        valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"{posicao:>2}. {fornecedor:<50} {valor_fmt}")


if __name__ == "__main__":
    main()
