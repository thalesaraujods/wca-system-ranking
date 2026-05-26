from io import BytesIO

import pandas as pd


def build_xlsx(df: pd.DataFrame, ranking: pd.DataFrame) -> bytes:
    """Build the circuit ranking workbook."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        ranking.to_excel(writer, sheet_name="Ranking Geral", index=False)
        df.to_excel(writer, sheet_name="Detalhes", index=False)

        workbook = writer.book
        fmt_header = workbook.add_format(
            {"bold": True, "bg_color": "#F1F5F9", "border": 1, "font_size": 10}
        )

        for sheet_name in ["Ranking Geral", "Detalhes"]:
            ws = writer.sheets[sheet_name]
            ws.set_column(0, 10, 20)
            ws.freeze_panes(1, 0)

            for col, value in enumerate(
                ranking.columns if sheet_name == "Ranking Geral" else df.columns
            ):
                ws.write(0, col, value, fmt_header)

    return output.getvalue()
