# API de Dados Abertos da Câmara — Exercícios

Scripts em Python para consumir a [API de Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/swagger/api.html).

## Requisitos

- `requests` (já disponível no ambiente)
- `nltk` (opcional, usado no script 4; se não estiver instalado, uma lista de stop words em português embutida é usada como alternativa)

## Arquivos

- `camara_api.py` — funções auxiliares: `get_paginado()` percorre automaticamente todas as páginas de um endpoint seguindo o link `rel="next"` retornado pela API, e `buscar_deputado_por_nome()` localiza um deputado pelo nome.
- `1_deputados_por_partido_uf.py PARTIDO UF` — lista deputados de um partido em um estado.
- `2_gastos_deputado_ano.py "NOME" ANO` — soma o valor líquido das despesas da cota parlamentar de um deputado em um ano.
- `3_maiores_fornecedores.py "NOME" ANO [TOP_N]` — ranking de fornecedores que mais receberam recursos da cota parlamentar.
- `4_analise_discursos.py "NOME" DATA_INICIO DATA_FIM [TOP_N]` — frequência de palavras nos discursos de um deputado no período, sem stop words.

## Exemplos

```bash
python3 1_deputados_por_partido_uf.py PL SP
python3 1_deputados_por_partido_uf.py PT MA

python3 2_gastos_deputado_ano.py "Tabata Amaral" 2026

python3 3_maiores_fornecedores.py "Tabata Amaral" 2026

python3 4_analise_discursos.py "Tabata Amaral" 2023-01-01 2026-08-14
```

## Observação sobre o endpoint de despesas

O endpoint `/deputados/{id}/despesas` só retorna dados quando o parâmetro
`idLegislatura` é informado explicitamente — sem ele, a API responde com uma
lista vazia mesmo havendo despesas registradas. Os scripts 2 e 3 tratam isso
automaticamente, usando a legislatura atual do deputado (`idLegislatura`
retornado por `/deputados?nome=...`).

## Paginação

Todas as consultas usam `get_paginado()`, que acumula os itens de `dados` e
segue o link com `rel="next"` em `links` até que ele deixe de existir,
garantindo que nenhuma página seja perdida em consultas com muitos resultados.
