"""2. Calcula o total gasto com a cota parlamentar de um deputado em um ano específico.

Exemplo de uso:
    python3 2_gastos_deputado_ano.py "Tabata Amaral" 2026
"""

import sys

from camara_api import buscar_deputado_por_nome, get_paginado


def total_gasto_no_ano(id_deputado, id_legislatura, ano):
    despesas = get_paginado(
        f"/deputados/{id_deputado}/despesas",
        {"ano": ano, "idLegislatura": id_legislatura},
    )
    return sum(despesa["valorLiquido"] for despesa in despesas), despesas


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "Tabata Amaral"
    ano = int(sys.argv[2]) if len(sys.argv) > 2 else 2026

    deputado = buscar_deputado_por_nome(nome)
    total, despesas = total_gasto_no_ano(deputado["id"], deputado["idLegislatura"], ano)

    print(f"Deputado(a): {deputado['nome']} ({deputado['siglaPartido']}-{deputado['siglaUf']})")
    print(f"Ano: {ano}")
    print(f"Quantidade de despesas: {len(despesas)}")
    print(f"Valor líquido total: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


if __name__ == "__main__":
    main()
