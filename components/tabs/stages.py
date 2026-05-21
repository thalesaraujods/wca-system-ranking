import pandas as pd
import streamlit as st
from utils.scoring import build_stage_ranking
from services.wca_api import CIRCUIT_COMPETITIONS


def render_stages_tab(df: pd.DataFrame, stages_meta: dict) -> None:
    if df.empty or "Etapa" not in df.columns:
        st.info("Nenhum dado de etapa disponível.")
        return

    stage_names = list(CIRCUIT_COMPETITIONS.keys())

    # ── Seção 1: Ranking por etapa ────────────────────────────────────────────
    st.subheader("Ranking por Etapa")
    _render_stage_summary_cards(df, stage_names, stages_meta)

    # ── Seção 2: Competidores de cada etapa ───────────────────────────────────
    st.divider()
    st.subheader("Competidores por Etapa")
    _render_stage_competitors(df, stage_names)

    # ── Seção 3: Participação no circuito ─────────────────────────────────────
    st.divider()
    st.subheader("Participação no Circuito")
    _render_participation_summary(df, stage_names)


# ─────────────────────────────────────────────────────────────────────────────

def _render_stage_summary_cards(
    df: pd.DataFrame, stage_names: list, stages_meta: dict
) -> None:
    cols = st.columns(len(stage_names))

    for col, stage_name in zip(cols, stage_names):
        with col:
            comp_name = stages_meta.get(stage_name) or stage_name
            stage_df = df[df["Etapa"] == stage_name]

            n_competitors = stage_df["Nome"].nunique() if not stage_df.empty else 0
            n_events = stage_df["Evento"].nunique() if not stage_df.empty else 0

            st.markdown(f"**{stage_name}**")
            st.caption(f"{comp_name} · {n_competitors} competidores · {n_events} eventos")

            if stage_df.empty:
                st.info("Resultados ainda não disponíveis.")
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
    # Seletor de etapa
    selected_stage = st.radio(
        label="Etapa",
        options=stage_names,
        horizontal=True,
        key="radio_stage_competitors",
    )

    stage_df = df[df["Etapa"] == selected_stage]

    if stage_df.empty:
        st.info(f"Nenhum resultado disponível para {selected_stage}.")
        return

    competitors = sorted(stage_df["Nome"].unique())
    n = len(competitors)

    # Linha de controles: filtro + toggle
    col_search, col_toggle = st.columns([3, 1])
    with col_search:
        search = st.selectbox(
            label="Filtrar competidor",
            options=["Todos"] + competitors,
            key="selectbox_stage_competitor_filter",
        )
    with col_toggle:
        show_detail = st.toggle(
            "Ver por evento",
            value=False,
            key="toggle_stage_detail",
        )

    st.caption(f"{n} competidores em {selected_stage}")

    # Filtra por competidor se selecionado
    if search != "Todos":
        stage_df = stage_df[stage_df["Nome"] == search]

    if show_detail:
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
    st.caption(
        f"{len(all_competitors)} competidores no total · "
        f"**{len(both)}** em ambas as etapas"
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
