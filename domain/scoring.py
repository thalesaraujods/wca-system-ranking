from typing import Optional

import pandas as pd

from domain.models import RoundResult


def calculate_points(total_competitors: int, position: Optional[int]) -> float:
    """Pt = TC / (P + 1), APS scoring formula."""
    if position is None or total_competitors == 0:
        return 0.0
    return round(total_competitors / (position + 1), 2)


def extract_person_identity(person: dict) -> tuple[str, str]:
    """Return a stable-ish competitor identity and the display name."""
    name = person.get("name", "")
    competitor_id = (
        person.get("wcaId")
        or person.get("registrantId")
        or person.get("id")
        or name
    )
    return str(competitor_id), name


def build_round_results(
    competition_data: dict,
    stage_name: Optional[str] = None,
) -> list[RoundResult]:
    """Convert raw WCA Live API response into normalized round results."""
    rows = []
    for event in competition_data.get("competitionEvents", []):
        event_name = event["event"]["name"]
        for rd in event.get("rounds", []):
            round_number = rd["number"]
            round_label = f"{event_name} — R{round_number}"
            results = rd.get("results", [])
            total_competitors = len(results)

            for res in results:
                position = res.get("ranking")
                if position is None:
                    continue

                competitor_id, competitor_name = extract_person_identity(
                    res.get("person", {})
                )
                rows.append(
                    RoundResult(
                        stage=stage_name,
                        event=event_name,
                        round_label=round_label,
                        competitor_id=competitor_id,
                        competitor_name=competitor_name,
                        position=position,
                        total_competitors=total_competitors,
                        points=calculate_points(total_competitors, position),
                    )
                )
    return rows


def build_dataframe(
    competition_data: dict,
    stage_name: Optional[str] = None,
) -> pd.DataFrame:
    """Convert raw WCA Live API response into the UI scoring DataFrame."""
    records = []
    for result in build_round_results(competition_data, stage_name):
        row = {
            "Competidor ID": result.competitor_id,
            "Evento": result.event,
            "Rodada": result.round_label,
            "Nome": result.competitor_name,
            "Posição": result.position,
            "TC": result.total_competitors,
            "Pontos": result.points,
        }
        if result.stage:
            row["Etapa"] = result.stage
        records.append(row)
    return pd.DataFrame(records)


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
    """Aggregate total points per competitor and assign dense ranks."""
    if df.empty:
        return pd.DataFrame(columns=["#", "Competidor", "Pontos Totais"])

    if "Competidor ID" in df.columns:
        ranking = (
            df.groupby("Competidor ID", as_index=False)
            .agg({"Nome": "first", "Pontos": "sum"})
            .sort_values(["Pontos", "Nome"], ascending=[False, True])
            .reset_index(drop=True)
        )
    else:
        ranking = (
            df.groupby("Nome", as_index=False)["Pontos"]
            .sum()
            .sort_values(["Pontos", "Nome"], ascending=[False, True])
            .reset_index(drop=True)
        )

    ranking["Pontos Totais"] = ranking["Pontos"].round(2)
    ranking["#"] = ranking["Pontos Totais"].rank(method="dense", ascending=False).astype(int)
    ranking = ranking.rename(columns={"Nome": "Competidor"})

    columns = ["#", "Competidor", "Pontos Totais"]
    return ranking[columns]


def build_stage_ranking(df: pd.DataFrame, stage_name: str) -> pd.DataFrame:
    """Aggregate points for a specific stage and assign dense ranks."""
    stage_df = df[df["Etapa"] == stage_name] if "Etapa" in df.columns else df
    if stage_df.empty:
        return pd.DataFrame(columns=["#", "Competidor", "Pontos na Etapa"])

    if "Competidor ID" in stage_df.columns:
        ranking = (
            stage_df.groupby("Competidor ID", as_index=False)
            .agg({"Nome": "first", "Pontos": "sum"})
            .sort_values(["Pontos", "Nome"], ascending=[False, True])
            .reset_index(drop=True)
        )
    else:
        ranking = (
            stage_df.groupby("Nome", as_index=False)["Pontos"]
            .sum()
            .sort_values(["Pontos", "Nome"], ascending=[False, True])
            .reset_index(drop=True)
        )

    ranking["Pontos na Etapa"] = ranking["Pontos"].round(2)
    ranking["#"] = ranking["Pontos na Etapa"].rank(method="dense", ascending=False).astype(int)
    ranking = ranking.rename(columns={"Nome": "Competidor"})

    columns = ["#", "Competidor", "Pontos na Etapa"]
    return ranking[columns]
