import pandas as pd
import streamlit as st


def render_rounds_tab(df: pd.DataFrame) -> None:
    """Results filtered by a selected round."""
    if df.empty:
        st.info("Nenhuma rodada disponível.")
        return

    if "Etapa" in df.columns:
        stages = sorted(df["Etapa"].unique())
        selected_stage = st.selectbox(
            label="Etapa",
            options=stages,
            key="selectbox_rounds_stage",
        )
        round_df = df[df["Etapa"] == selected_stage]
    else:
        selected_stage = None
        round_df = df

    rounds = sorted(round_df["Rodada"].unique())
    selected_round = st.selectbox(
        label="Evento / Rodada",
        options=rounds,
        key="selectbox_rounds",
    )

    filtered = (
        round_df[round_df["Rodada"] == selected_round][["Posição", "Nome", "TC", "Pontos"]]
        .sort_values("Posição")
        .reset_index(drop=True)
    )
    filtered.insert(0, "#", range(1, len(filtered) + 1))

    tc_value = filtered["TC"].iloc[0] if not filtered.empty else 0
    st.markdown(
        f'<p class="tab-meta">{tc_value} competidores nesta rodada'
        f'{f" · {selected_stage}" if selected_stage else ""}</p>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        filtered[["#", "Nome", "Posição", "Pontos"]],
        width="stretch",
        hide_index=True,
        column_config={
            "#": st.column_config.NumberColumn(width="small", format="%d"),
            "Nome": st.column_config.TextColumn(width="large"),
            "Posição": st.column_config.NumberColumn(width="small", format="%d"),
            "Pontos": st.column_config.NumberColumn(format="%.2f", width="medium"),
        },
    )
