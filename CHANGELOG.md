# Changelog — wca-sr

---

## v2.0.0 — Circuito dos Shoppings (2026-05-21)

### Identidade Visual

- **Nova paleta de cores** baseada no brand do *Circuito dos Shoppings*:
  - Verde floresta `#3B6E48` como cor primária (substituiu o índigo)
  - Âmbar terroso `#B87830` como cor secundária (botão de exportação, destaque de etapa)
  - Fundo creme `#F2EDE6` (substituiu o slate neutro)
  - Texto principal em verde escuro `#1C3A27`
- **Logo** `logo-circuito.png` adicionada ao header em destaque centralizado
- `config.toml` atualizado com os novos tokens de tema

### Nomenclatura e Descrição

- Título do sistema atualizado para **"Ranking — Circuito dos Shoppings"**
- `page_title` do Streamlit atualizado para `"Ranking — Circuito dos Shoppings"`
- `page_icon` alterado para `🏆`
- Descrição adicionada ao header:
  > *"Este ranking apura os campeões gerais do circuito com base nos resultados
  > combinados da Etapa Sumaúma e da Etapa Ponta Negra."*

### Competições Fixas

- Removido o formulário de entrada de URL
- As duas etapas do circuito são carregadas automaticamente via botão "Carregar resultados do circuito":
  | Etapa | ID WCA Live |
  |-------|-------------|
  | Etapa Sumaúma | `10694` |
  | Etapa Ponta Negra | `10695` |
- Adicionada função `fetch_all_circuit_stages()` em `services/wca_api.py`
- Adicionada constante `CIRCUIT_COMPETITIONS` com os IDs fixos
- Dados das duas etapas são combinados em um único DataFrame com coluna `Etapa`
- Adicionadas funções `build_combined_dataframe()` e `build_stage_ranking()` em `utils/scoring.py`

### Nova Aba "Por Etapa"

- Adicionado arquivo `components/tabs/stages.py`
- A aba exibe lado a lado:
  - Ranking de pontuação de cada etapa individualmente
  - Número de competidores e eventos por etapa
- Tabela de **Participação no Circuito** abaixo das colunas:
  - Lista todos os competidores
  - Indica em quais etapas cada um participou (`✓` / `—`)
  - Informa quantas etapas cada competidor completou (`X/2`)
  - Ordenada: competidores com ambas as etapas aparecem primeiro

### Ordem das Abas

| Antes | Depois |
|-------|--------|
| Ranking Geral | Ranking Geral |
| Por Rodada | **Por Etapa** ← novo |
| Individual | Por Rodada |
| Exportar | Individual |
| — | Exportar |

### Arquivos Modificados

| Arquivo | Tipo de mudança |
|---------|----------------|
| `app.py` | Reescrito — novo fluxo, paleta, abas |
| `components/header.py` | Reescrito — logo + título + descrição |
| `services/wca_api.py` | Adicionado `CIRCUIT_COMPETITIONS` e `fetch_all_circuit_stages()` |
| `utils/scoring.py` | Adicionado `build_combined_dataframe()` e `build_stage_ranking()` |
| `.streamlit/config.toml` | Atualizado com paleta do circuito |
| `logo-circuito.png` | Adicionado ao diretório raiz |

### Arquivos Criados

| Arquivo | Descrição |
|---------|-----------|
| `components/tabs/stages.py` | Nova aba "Por Etapa" |
| `CHANGELOG.md` | Este arquivo |

---

## v1.0.0 — wca-sr inicial (2026-05-20)

- Sistema base com busca por URL de competição
- Abas: Ranking Geral, Por Rodada, Individual, Exportar
- Design system minimalista (índigo + slate)
- Compatibilidade com Python 3.9+
