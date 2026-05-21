import pandas as pd
import streamlit as st


def render_individual_tab(df: pd.DataFrame, ranking: pd.DataFrame) -> None:
    """Individual competitor panorama: metrics + round-by-round detail."""
    if df.empty:
        st.info("Nenhum dado disponível.")
        return

    competitors = sorted(df["Nome"].unique())
    selected = st.selectbox(
        label="Competidor",
        options=competitors,
        key="selectbox_individual",
    )

    total_pts = ranking.loc[ranking["Competidor"] == selected, "Pontos Totais"]
    total_pts_val = float(total_pts.values[0]) if not total_pts.empty else 0.0

    position = ranking.loc[ranking["Competidor"] == selected, "#"]
    position_val = int(position.values[0]) if not position.empty else "-"
    position_str = f"{position_val}.º"

    col_total, col_pos = st.columns(2)
    with col_total:
        st.metric(label="Pontos Totais", value=f"{total_pts_val:.2f}")
    with col_pos:
        st.metric(label="Posição Geral", value=position_str)

    detail = (
        df[df["Nome"] == selected][["Evento", "Rodada", "Posição", "TC", "Pontos"]]
        .sort_values(["Evento", "Rodada"])
        .reset_index(drop=True)
    )

    st.dataframe(
        detail,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Evento": st.column_config.TextColumn(width="medium"),
            "Rodada": st.column_config.TextColumn(width="large"),
            "Posição": st.column_config.NumberColumn(width="small", format="%d"),
            "TC": st.column_config.NumberColumn(
                label="Total Competidores", width="small", format="%d"
            ),
            "Pontos": st.column_config.NumberColumn(format="%.2f", width="medium"),
        },
    )
