from datetime import date
from io import BytesIO

import pandas as pd
import streamlit as st


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
        xlsx_bytes = _build_xlsx(df, ranking)
        filename = f"wca-sr_{competition_id}_{date.today()}.xlsx"
        st.download_button(
            label="Baixar planilha (.xlsx)",
            data=xlsx_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
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


def _build_xlsx(df: pd.DataFrame, ranking: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        ranking.to_excel(writer, sheet_name="Ranking Geral", index=False)
        df.to_excel(writer, sheet_name="Detalhes", index=False)

        workbook = writer.book
        fmt_header = workbook.add_format(
            {"bold": True, "bg_color": "#F1F5F9", "border": 1, "font_size": 10}
        )
        fmt_number = workbook.add_format({"num_format": "0.00", "align": "right"})

        for sheet_name in ["Ranking Geral", "Detalhes"]:
            ws = writer.sheets[sheet_name]
            ws.set_column(0, 10, 20)
            ws.freeze_panes(1, 0)

    return output.getvalue()
