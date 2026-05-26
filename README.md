# Ranking — Circuito dos Shoppings

> Sistema de classificação geral para o **Circuito dos Shoppings de Cubo Mágico**,
> apurando os campeões com base nos resultados combinados da **Etapa Sumaúma** e da **Etapa Ponta Negra**.

![Python](https://img.shields.io/badge/Python-3.9+-3B6E48?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-B87830?style=flat-square&logo=streamlit&logoColor=white)
![WCA](https://img.shields.io/badge/WCA_Live-API-3B6E48?style=flat-square)

---

## Sobre o projeto

O **Ranking — Circuito dos Shoppings** é uma aplicação web desenvolvida em Streamlit que consome dados em tempo real da [WCA Live API](https://live.worldcubeassociation.org) para calcular a classificação geral dos competidores do circuito.

A pontuação segue a fórmula criada pela **APS (Associação Portuguesa de Speedcubing)**:

$$Pt = \frac{TC}{P + 1}$$

| Variável | Descrição |
|----------|-----------|
| **Pt** | Pontos obtidos na rodada |
| **TC** | Total de competidores na rodada |
| **P** | Posição do competidor na rodada |

O ranking final é a **soma dos pontos** obtidos em todas as rodadas de ambas as etapas.
Em caso de empate na pontuação total, o sistema usa **ranking denso**:
competidores empatados recebem a mesma posição e a próxima posição não deixa lacuna.

As etapas do circuito ficam configuradas em [`config/circuit.json`](config/circuit.json),
permitindo reutilizar a aplicação para outros circuitos sem alterar o código Python.

---

## Etapas do Circuito

| Etapa | Competição WCA Live |
|-------|---------------------|
| Etapa Sumaúma | [#10694](https://live.worldcubeassociation.org/competitions/10694) |
| Etapa Ponta Negra | [#10695](https://live.worldcubeassociation.org/competitions/10695) |

---

## Funcionalidades

- **Ranking Geral** — classificação combinada das duas etapas, ordenada por pontuação total
- **Por Etapa** — visualização separada de cada etapa com:
  - Ranking de pontos por etapa
  - Lista completa de competidores com filtro e visão detalhada por evento/rodada
  - Tabela de participação mostrando quem disputou ambas as etapas
- **Por Rodada** — resultados filtrados por evento e rodada específica
- **Individual** — panorama completo de um competidor (pontos totais, posição geral, detalhamento por rodada)
- **Exportar** — download da planilha `.xlsx` com ranking geral e detalhes por rodada

---

## Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| [Streamlit](https://streamlit.io) | Interface web |
| [Pandas](https://pandas.pydata.org) | Manipulação de dados |
| [Requests](https://requests.readthedocs.io) | Consumo da API GraphQL |
| [XlsxWriter](https://xlsxwriter.readthedocs.io) | Geração de planilhas Excel |
| WCA Live GraphQL API | Dados de competição em tempo real |

---

## Instalação e execução

### Pré-requisitos

- Python 3.9 ou superior
- pip

### Passos

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd wca-sr

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie o app
streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## Estrutura do projeto

```
wca-sr/
├── app.py                         # Entrypoint principal
├── requirements.txt               # Dependências Python
├── config/
│   ├── circuit.json               # Etapas e metadados do circuito
│   └── circuit.py                 # Loader tipado da configuração
├── domain/
│   ├── models.py                  # Modelos normalizados do domínio
│   └── scoring.py                 # Fórmula, ranking e transformação dos dados
├── banner-circuito.jpg            # Banner do circuito (header)
├── logo-circuito.png              # Logo alternativa
├── .streamlit/
│   └── config.toml                # Tema e configurações do Streamlit
├── components/
│   ├── header.py                  # Cabeçalho com banner e descrição
│   ├── search.py                  # (Reservado) formulário de busca
│   └── tabs/
│       ├── ranking.py             # Aba: Ranking Geral
│       ├── stages.py              # Aba: Por Etapa
│       ├── rounds.py              # Aba: Por Rodada
│       ├── individual.py          # Aba: Individual
│       └── export.py              # Aba: Exportar
├── services/
│   ├── wca_api.py                 # Cliente GraphQL WCA Live
│   └── exporter.py                # Geração da planilha Excel
├── utils/
│   └── scoring.py                 # Compatibilidade para imports antigos
├── tests/
│   └── test_scoring.py            # Testes da regra de pontuação e ranking
├── CHANGELOG.md                   # Histórico de versões
└── README.md                      # Este arquivo
```

---

## Créditos

| Contribuição | Responsável |
|---|---|
| Fórmula de pontuação | [APS — Associação Portuguesa de Speedcubing](https://www.instagram.com/p/DS-H9wJiAoi) |
| Organização do circuito | AACM — Associação Amazonense de Cubo Mágico |
| Regulamento oficial | [World Cube Association](https://www.worldcubeassociation.org) |

---

*Desenvolvido para o Circuito dos Shoppings — Etapa Sumaúma & Ponta Negra.*
