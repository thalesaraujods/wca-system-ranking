from datetime import date

import pandas as pd
import streamlit as st

from services.exporter import build_xlsx


def render_export_tab(
    df: pd.DataFrame,
    ranking: pd.DataFrame,
    competition_id: str,
    competition_name: str,
) -> None:
    """Export tab — generates and offers the .xlsx download."""
    n_competitors = ranking["Competidor"].nunique()
    n_events = df["Evento"].nunique()
    n_rounds = df["Rodada"].nunique()

    st.markdown(
        f"""
        <div class="export-summary">
            <p class="export-competition">{competition_name}</p>
            <p class="tab-meta">
                {n_competitors} competidores · {n_events} eventos · {n_rounds} rodadas
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        xlsx_bytes = build_xlsx(df, ranking)
        filename = f"wca-sr_{competition_id}_{date.today()}.xlsx"
        st.download_button(
            label="Baixar planilha (.xlsx)",
            data=xlsx_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            width="stretch",
            key="btn_download",
        )

    st.markdown(
        """
        <div class="export-info">
            <p class="tab-meta">O arquivo inclui:</p>
            <ul class="export-list">
                <li><strong>Ranking Geral</strong> — pontuação total por competidor</li>
                <li><strong>Detalhes</strong> — pontuação por evento e rodada</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
