"""Funções auxiliares para consumir a API de Dados Abertos da Câmara dos Deputados.

Documentação: https://dadosabertos.camara.leg.br/swagger/api.html
"""

import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def get_paginado(caminho, params=None):
    """Busca todas as páginas de um endpoint da API e retorna a lista completa de itens.

    A API pagina as respostas e indica a próxima página através de um link
    com rel="next" dentro do campo "links" do corpo JSON. Este helper segue
    esses links até que não exista mais uma próxima página.
    """
    if params is None:
        params = {}

    itens = []
    url = f"{BASE_URL}{caminho}"
    params_atual = {"itens": 100, "pagina": 1, **params, "formato": "json"}

    while url:
        resposta = requests.get(url, params=params_atual)
        resposta.raise_for_status()
        corpo = resposta.json()

        itens.extend(corpo.get("dados", []))

        proximo = next(
            (link["href"] for link in corpo.get("links", []) if link["rel"] == "next"),
            None,
        )
        url = proximo
        params_atual = None  # os parâmetros já vêm embutidos no link "next"

    return itens


def buscar_deputado_por_nome(nome):
    """Retorna os dados básicos do primeiro deputado encontrado com o nome informado."""
    resultados = get_paginado("/deputados", {"nome": nome})
    if not resultados:
        raise ValueError(f"Nenhum deputado encontrado com o nome '{nome}'.")
    return resultados[0]
