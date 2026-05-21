import pandas as pd
from typing import Optional


def calculate_points(total_competitors: int, position: int) -> float:
    """Pt = TC / (P + 1) — APS scoring formula."""
    if position is None or total_competitors == 0:
        return 0.0
    return round(total_competitors / (position + 1), 2)


def build_dataframe(competition_data: dict, stage_name: Optional[str] = None) -> pd.DataFrame:
    """
    Convert raw WCA Live API response into the scoring DataFrame.
    Optionally tags each row with a stage_name.
    """
    rows = []
    for event in competition_data.get("competitionEvents", []):
        event_name = event["event"]["name"]
        for rd in event.get("rounds", []):
            round_number = rd["number"]
            round_label = f"{event_name} — R{round_number}"
            results = rd.get("results", [])
            tc = len(results)
            for res in results:
                if res.get("ranking") is None:
                    continue
                position = res["ranking"]
                row = {
                    "Evento": event_name,
                    "Rodada": round_label,
                    "Nome": res["person"]["name"],
                    "Posição": position,
                    "TC": tc,
                    "Pontos": calculate_points(tc, position),
                }
                if stage_name:
                    row["Etapa"] = stage_name
                rows.append(row)
    return pd.DataFrame(rows)


def build_combined_dataframe(stages_data: dict) -> pd.DataFrame:
    """
    Build a combined DataFrame from all circuit stages.
    stages_data: { stage_name: competition_data }
    """
    frames = []
    for stage_name, data in stages_data.items():
        if data is None:
            continue
        df = build_dataframe(data, stage_name=stage_name)
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def build_general_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total points per competitor and assign rank."""
    if df.empty:
        return pd.DataFrame(columns=["#", "Competidor", "Pontos Totais"])
    ranking = (
        df.groupby("Nome")["Pontos"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    ranking.columns = ["Competidor", "Pontos Totais"]
    ranking["Pontos Totais"] = ranking["Pontos Totais"].round(2)
    ranking.insert(0, "#", range(1, len(ranking) + 1))
    return ranking


def build_stage_ranking(df: pd.DataFrame, stage_name: str) -> pd.DataFrame:
    """Aggregate points for a specific stage and assign rank."""
    stage_df = df[df["Etapa"] == stage_name] if "Etapa" in df.columns else df
    if stage_df.empty:
        return pd.DataFrame(columns=["#", "Competidor", "Pontos na Etapa"])
    ranking = (
        stage_df.groupby("Nome")["Pontos"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    ranking.columns = ["Competidor", "Pontos na Etapa"]
    ranking["Pontos na Etapa"] = ranking["Pontos na Etapa"].round(2)
    ranking.insert(0, "#", range(1, len(ranking) + 1))
    return ranking
