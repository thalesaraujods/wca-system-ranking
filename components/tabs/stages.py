import pandas as pd
import streamlit as st
from utils.scoring import build_stage_ranking
from services.wca_api import CIRCUIT_COMPETITIONS


def render_stages_tab(df: pd.DataFrame, stages_meta: dict) -> None:
    """
    Show competitors and scores broken down by circuit stage.
    stages_meta: { stage_name: competition_name | None }
    """
    if df.empty or "Etapa" not in df.columns:
        st.info("Nenhum dado de etapa disponível.")
        return

    stage_names = list(CIRCUIT_COMPETITIONS.keys())

    # ── Seção 1: Cards de resumo por etapa ───────────────────────────────────
    _render_stage_summary_cards(df, stage_names, stages_meta)

    st.divider()

    # ── Seção 2: Competidores de cada etapa ──────────────────────────────────
    _render_stage_competitors(df, stage_names)

    st.divider()

    # ── Seção 3: Participação geral no circuito ───────────────────────────────
    _render_participation_summary(df, stage_names)


# ─────────────────────────────────────────────────────────────────────────────

def _render_stage_summary_cards(
    df: pd.DataFrame, stage_names: list, stages_meta: dict
) -> None:
    """Side-by-side ranking cards — one per stage."""
    cols = st.columns(len(stage_names))

    for col, stage_name in zip(cols, stage_names):
        with col:
            comp_name = stages_meta.get(stage_name) or stage_name
            stage_df = df[df["Etapa"] == stage_name]

            n_competitors = stage_df["Nome"].nunique() if not stage_df.empty else 0
            n_events = stage_df["Evento"].nunique() if not stage_df.empty else 0

            st.markdown(
                f"""
                <div class="stage-card">
                    <p class="stage-title">{stage_name}</p>
                    <p class="tab-meta">{comp_name}</p>
                    <p class="tab-meta">{n_competitors} competidores · {n_events} eventos</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if stage_df.empty:
                st.markdown(
                    '<p class="tab-meta">Resultados ainda não disponíveis.</p>',
                    unsafe_allow_html=True,
                )
                continue

            ranking = build_stage_ranking(df, stage_name)
            st.dataframe(
                ranking,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "#": st.column_config.NumberColumn(width="small", format="%d"),
                    "Competidor": st.column_config.TextColumn(width="large"),
                    "Pontos na Etapa": st.column_config.NumberColumn(
                        format="%.2f", width="medium"
                    ),
                },
            )


def _render_stage_competitors(df: pd.DataFrame, stage_names: list) -> None:
    """
    Interactive section: choose a stage, see all competitors with
    their event-by-event breakdown.
    """
    st.markdown(
        '<p class="stage-title">Competidores por Etapa</p>',
        unsafe_allow_html=True,
    )

    # Seletor de etapa
    selected_stage = st.radio(
        label="Selecione a etapa",
        options=stage_names,
        horizontal=True,
        key="radio_stage_competitors",
        label_visibility="collapsed",
    )

    stage_df = df[df["Etapa"] == selected_stage]

    if stage_df.empty:
        st.info(f"Nenhum resultado disponível para {selected_stage}.")
        return

    competitors = sorted(stage_df["Nome"].unique())
    n = len(competitors)

    st.markdown(
        f'<p class="tab-meta">{n} competidores inscrito(s) em {selected_stage}</p>',
        unsafe_allow_html=True,
    )

    # Opção de filtrar por competidor
    col_search, col_toggle = st.columns([3, 1])
    with col_search:
        search = st.selectbox(
            label="Filtrar competidor",
            options=["Todos"] + competitors,
            key="selectbox_stage_competitor_filter",
            label_visibility="collapsed",
        )
    with col_toggle:
        show_detail = st.toggle(
            "Ver por evento",
            value=False,
            key="toggle_stage_detail",
        )

    # Filtra se selecionou um competidor específico
    if search != "Todos":
        stage_df = stage_df[stage_df["Nome"] == search]

    if show_detail:
        # Visão detalhada: evento · rodada · posição · TC · pontos
        detail = (
            stage_df[["Nome", "Evento", "Rodada", "Posição", "TC", "Pontos"]]
            .sort_values(["Nome", "Evento", "Rodada"])
            .reset_index(drop=True)
        )
        st.dataframe(
            detail,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nome": st.column_config.TextColumn(width="medium"),
                "Evento": st.column_config.TextColumn(width="medium"),
                "Rodada": st.column_config.TextColumn(width="large"),
                "Posição": st.column_config.NumberColumn(width="small", format="%d"),
                "TC": st.column_config.NumberColumn(
                    label="Total Comp.", width="small", format="%d"
                ),
                "Pontos": st.column_config.NumberColumn(format="%.2f", width="small"),
            },
        )
    else:
        # Visão resumida: competidor · total de pontos na etapa
        summary = (
            stage_df.groupby("Nome")["Pontos"]
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .reset_index()
        )
        summary.columns = ["Competidor", "Pontos na Etapa"]
        summary.insert(0, "#", range(1, len(summary) + 1))

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "#": st.column_config.NumberColumn(width="small", format="%d"),
                "Competidor": st.column_config.TextColumn(width="large"),
                "Pontos na Etapa": st.column_config.NumberColumn(
                    format="%.2f", width="medium"
                ),
            },
        )


def _render_participation_summary(df: pd.DataFrame, stage_names: list) -> None:
    """Show which competitors participated in each stage."""
    st.markdown(
        '<p class="stage-title">Participação no Circuito</p>',
        unsafe_allow_html=True,
    )

    sets = {}
    for sn in stage_names:
        stage_df = df[df["Etapa"] == sn]
        sets[sn] = set(stage_df["Nome"].unique()) if not stage_df.empty else set()

    all_competitors = set().union(*sets.values())

    rows = []
    for name in sorted(all_competitors):
        row = {"Competidor": name}
        for sn in stage_names:
            row[sn] = "✓" if name in sets[sn] else "—"
        participated_in = sum(1 for sn in stage_names if name in sets[sn])
        row["Etapas"] = f"{participated_in}/{len(stage_names)}"
        rows.append(row)

    summary_df = pd.DataFrame(rows)
    summary_df["_sort"] = summary_df["Etapas"].apply(
        lambda x: -int(x.split("/")[0])
    )
    summary_df = (
        summary_df.sort_values("_sort")
        .drop(columns=["_sort"])
        .reset_index(drop=True)
    )

    both = summary_df[summary_df["Etapas"] == f"{len(stage_names)}/{len(stage_names)}"]
    st.markdown(
        f'<p class="tab-meta">'
        f'{len(all_competitors)} competidores no total · '
        f'<strong>{len(both)} em ambas as etapas</strong>'
        f'</p>',
        unsafe_allow_html=True,
    )

    col_config = {
        "Competidor": st.column_config.TextColumn(width="large"),
        "Etapas": st.column_config.TextColumn(width="small"),
    }
    for sn in stage_names:
        col_config[sn] = st.column_config.TextColumn(width="medium")

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        column_config=col_config,
    )
