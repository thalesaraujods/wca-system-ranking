import streamlit as st

from components.header import render_header
from components.tabs.export import render_export_tab
from components.tabs.individual import render_individual_tab
from components.tabs.ranking import render_ranking_tab
from components.tabs.rounds import render_rounds_tab
from components.tabs.stages import render_stages_tab
from services.wca_api import fetch_all_circuit_stages, CIRCUIT_COMPETITIONS
from utils.scoring import build_combined_dataframe, build_general_ranking

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Ranking — Circuito dos Shoppings",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    :root {
        /* Paleta Circuito dos Shoppings */
        --color-green-dark:    #1C3A27;   /* texto principal, fundo escuro */
        --color-green-mid:     #3B6E48;   /* verde primário / accent */
        --color-green-light:   #5A9970;   /* hover, badges */
        --color-green-subtle:  #E6EFE9;   /* fundo sutil, zebra */

        --color-brown-dark:    #7A4A1E;   /* texto âmbar escuro */
        --color-brown-mid:     #B87830;   /* âmbar principal */
        --color-brown-light:   #D4A055;   /* hover âmbar, destaques */
        --color-brown-subtle:  #F5EDE0;   /* fundo âmbar sutil */

        --color-bg:            #F8F4F1;   /* fundo do banner */
        --color-surface:       #F8F4F1;   /* cards e tabelas */
        --color-surface-alt:   #F8F4F1;   /* zebra, inputs */
        --color-border:        #D8D0C4;   /* divisórias */
        --color-border-strong: #C4BAB0;   /* bordas de input */

        --color-text-primary:  #1C3A27;
        --color-text-secondary:#4A6355;
        --color-text-tertiary: #8A9E93;
        --color-text-inverse:  #FDFAF6;

        --color-success:       #2E7D52;
        --color-success-bg:    #E6F4EC;
        --color-warning:       #B87830;
        --color-warning-bg:    #FDF3E0;
        --color-error:         #C0392B;
        --color-error-bg:      #FDECEA;
        --color-info:          #3B6E48;
        --color-info-bg:       #E6EFE9;

        /* Ranking */
        --color-rank-gold:     #92700A;
        --color-rank-silver:   #5A7A6A;
        --color-rank-bronze:   #7A4A1E;

        --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
        --radius-sm: 6px;
        --radius-md: 10px;
        --border-thin: 1px solid var(--color-border);
        --shadow-xs: 0 1px 3px rgba(28,58,39,0.08);
        --shadow-sm: 0 2px 8px rgba(28,58,39,0.10);
        --focus-ring: 0 0 0 3px rgba(90,153,112,0.30);
    }

    /* ── Fundo da página ── */
    .stApp,
    .stApp > div,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    section[data-testid="stSidebar"],
    .main .block-container {
        background-color: var(--color-bg) !important;
    }

    /* ── Header do circuito ── */
    .circuit-header { text-align: center; margin: 0.5rem 0 1rem; }

    .circuit-ranking-title {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--color-green-dark) !important;
        letter-spacing: -0.01em;
        margin: 0.5rem 0 0.25rem !important;
    }

    .circuit-description {
        font-size: 0.9375rem !important;
        color: var(--color-text-secondary) !important;
        max-width: 560px;
        margin: 0 auto !important;
        line-height: 1.6 !important;
    }

    .circuit-title {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--color-green-dark) !important;
        text-align: center;
    }

    /* ── Divider ── */
    hr { border-color: var(--color-border) !important; margin: 1.25rem 0 !important; }

    /* ── Botão primário (verde) ── */
    .stButton > button[kind="primary"] {
        background-color: var(--color-green-mid) !important;
        color: var(--color-text-inverse) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        transition: background-color 150ms ease, box-shadow 150ms ease !important;
        box-shadow: var(--shadow-xs) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: var(--color-green-dark) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    .stButton > button[kind="primary"]:focus-visible {
        box-shadow: var(--focus-ring) !important;
        outline: none !important;
    }

    /* ── Botão secundário ── */
    .stButton > button[kind="secondary"] {
        background-color: var(--color-surface) !important;
        color: var(--color-green-dark) !important;
        border: 1px solid var(--color-border-strong) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: background-color 150ms ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--color-green-subtle) !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background-color: var(--color-brown-mid) !important;
        color: var(--color-text-inverse) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        transition: background-color 150ms ease, box-shadow 150ms ease !important;
        box-shadow: var(--shadow-xs) !important;
    }
    .stDownloadButton > button:hover {
        background-color: var(--color-brown-dark) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox label {
        font-size: 0.8125rem !important;
        font-weight: 500 !important;
        color: var(--color-text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-baseweb="select"] > div {
        border: 1px solid var(--color-border-strong) !important;
        border-radius: var(--radius-sm) !important;
        background: var(--color-surface) !important;
        font-size: 0.9375rem !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        border-bottom: 1px solid var(--color-border) !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        color: var(--color-text-secondary) !important;
        padding: 10px 18px !important;
        border-radius: 0 !important;
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        transition: color 150ms ease, border-color 150ms ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--color-green-dark) !important;
        border-bottom-color: var(--color-border) !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--color-green-dark) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--color-green-mid) !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

    /* ── DataFrames ── */
    .stDataFrame {
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        background: var(--color-surface) !important;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] thead th {
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: var(--color-text-tertiary) !important;
        background: var(--color-surface-alt, #F8F4F1) !important;
    }

    /* ── Métricas ── */
    [data-testid="metric-container"] {
        background: var(--color-surface) !important;
        border: var(--border-thin) !important;
        border-radius: var(--radius-md) !important;
        padding: 20px 24px !important;
        border-left: 4px solid var(--color-green-mid) !important;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: var(--color-text-tertiary) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: var(--font-mono) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--color-green-dark) !important;
    }

    /* ── Alerts ── */
    .stAlert {
        border-radius: var(--radius-sm) !important;
        font-size: 0.9375rem !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: var(--color-green-mid) !important; }

    /* ── Utility classes ── */
    .tab-meta {
        font-size: 0.8125rem !important;
        color: var(--color-text-tertiary) !important;
        margin-bottom: 10px !important;
    }

    .stage-title {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--color-green-dark) !important;
        margin-bottom: 4px !important;
        padding-bottom: 6px !important;
        border-bottom: 2px solid var(--color-brown-mid) !important;
    }

    .export-summary { margin-bottom: 24px; }
    .export-competition {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: var(--color-green-dark) !important;
        margin-bottom: 4px !important;
    }
    .export-info { margin-top: 20px; }
    .export-list {
        font-size: 0.875rem !important;
        color: var(--color-text-secondary) !important;
        margin-top: 6px !important;
        padding-left: 20px !important;
    }
    .export-list li { margin-bottom: 4px; }

    /* Banner de carregamento */
    .loading-banner {
        text-align: center;
        padding: 2.5rem 1rem;
        color: var(--color-text-secondary);
        font-size: 0.9375rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────

if "loaded" not in st.session_state:
    st.session_state.loaded = False
    st.session_state.df = None
    st.session_state.ranking = None
    st.session_state.stages_meta = {}

# ── Header ────────────────────────────────────────────────────────────────────

render_header()

# ── Carregamento automático das competições ───────────────────────────────────

if not st.session_state.loaded:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        load_btn = st.button(
            "Carregar resultados do circuito",
            type="primary",
            use_container_width=True,
            key="btn_load",
        )

    if load_btn:
        with st.spinner("Buscando resultados das etapas…"):
            stages_data = fetch_all_circuit_stages()

        # Verifica quais etapas retornaram dados
        stages_meta = {}
        any_loaded = False
        for stage_name, data in stages_data.items():
            if data is not None:
                stages_meta[stage_name] = data.get("name", stage_name)
                any_loaded = True
            else:
                stages_meta[stage_name] = None

        if not any_loaded:
            st.error(
                "Não foi possível conectar ao WCA Live. "
                "Verifique sua conexão ou tente novamente."
            )
        else:
            # Avança para a tela de resultados mesmo sem resultados publicados
            df = build_combined_dataframe(stages_data)
            st.session_state.df = df
            st.session_state.ranking = build_general_ranking(df)
            st.session_state.stages_meta = stages_meta
            st.session_state.loaded = True
            st.rerun()

    # Info sobre etapas que serão carregadas
    st.markdown(
        """
        <div class="loading-banner">
            Serão carregadas automaticamente:<br>
            <strong>Etapa Sumaúma</strong> e <strong>Etapa Ponta Negra</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Resultados ────────────────────────────────────────────────────────────────

else:
    df = st.session_state.df
    ranking = st.session_state.ranking
    stages_meta = st.session_state.stages_meta

    # Barra de status + botão de atualizar
    col_info, col_btn = st.columns([5, 1])
    with col_info:
        etapas_carregadas = [k for k, v in stages_meta.items() if v is not None]
        st.markdown(
            f'<p class="tab-meta">Circuito carregado · '
            f'{" e ".join(etapas_carregadas)}</p>',
            unsafe_allow_html=True,
        )
    with col_btn:
        if st.button("Atualizar", type="secondary", key="btn_reload"):
            st.session_state.loaded = False
            st.rerun()

    # Banner quando resultados ainda não foram publicados
    if df is None or df.empty:
        etapas_nomes = [v for v in stages_meta.values() if v]
        st.info(
            f"✅ Competições encontradas: **{' · '.join(etapas_nomes)}**\n\n"
            "Os resultados ainda não foram publicados no WCA Live. "
            "Clique em **Atualizar** quando a competição estiver em andamento."
        )
        st.stop()

    st.divider()

    tab_ranking, tab_stages, tab_rounds, tab_individual, tab_export = st.tabs(
        ["Ranking Geral", "Por Etapa", "Por Rodada", "Individual", "Exportar"]
    )

    with tab_ranking:
        render_ranking_tab(ranking)

    with tab_stages:
        render_stages_tab(df, stages_meta)

    with tab_rounds:
        render_rounds_tab(df)

    with tab_individual:
        render_individual_tab(df, ranking)

    with tab_export:
        render_export_tab(
            df,
            ranking,
            "CircuitoDosShoppings",
            "Ranking — Circuito dos Shoppings",
        )
