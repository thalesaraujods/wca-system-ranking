import pandas as pd
import streamlit as st


def render_ranking_tab(ranking: pd.DataFrame) -> None:
    """General ranking — all competitors sorted by total points."""
    if ranking.empty:
        st.info("Nenhum dado disponível para esta competição.")
        return

    total = len(ranking)
    st.markdown(
        f'<p class="tab-meta">{total} competidores</p>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True,
        column_config={
            "#": st.column_config.NumberColumn(width="small", format="%d"),
            "Competidor": st.column_config.TextColumn(width="large"),
            "Pontos Totais": st.column_config.NumberColumn(
                format="%.2f", width="medium"
            ),
        },
    )
