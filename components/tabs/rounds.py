import pandas as pd
import streamlit as st


def render_rounds_tab(df: pd.DataFrame) -> None:
    """Results filtered by a selected round."""
    if df.empty:
        st.info("Nenhuma rodada disponível.")
        return

    rounds = sorted(df["Rodada"].unique())
    selected = st.selectbox(
        label="Evento / Rodada",
        options=rounds,
        key="selectbox_rounds",
    )

    filtered = (
        df[df["Rodada"] == selected][["Posição", "Nome", "TC", "Pontos"]]
        .sort_values("Posição")
        .reset_index(drop=True)
    )
    filtered.insert(0, "#", range(1, len(filtered) + 1))

    tc_value = filtered["TC"].iloc[0] if not filtered.empty else 0
    st.markdown(
        f'<p class="tab-meta">{tc_value} competidores nesta rodada</p>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        filtered[["#", "Nome", "Posição", "Pontos"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "#": st.column_config.NumberColumn(width="small", format="%d"),
            "Nome": st.column_config.TextColumn(width="large"),
            "Posição": st.column_config.NumberColumn(width="small", format="%d"),
            "Pontos": st.column_config.NumberColumn(format="%.2f", width="medium"),
        },
    )
