import re
from typing import Optional

import requests

_API_URL = "https://live.worldcubeassociation.org/api/graphql"
_HEADERS = {
    "User-Agent": "wca-sr/1.0 (circuito-dos-shoppings)",
    "Content-Type": "application/json",
}
_QUERY = """
query GetCompetitionResults($id: ID!) {
  competition(id: $id) {
    name
    competitionEvents {
      event { name }
      rounds {
        id
        number
        results {
          ranking
          person { name }
        }
      }
    }
  }
}
"""

# Competições fixas do Circuito dos Shoppings
CIRCUIT_COMPETITIONS = {
    "Etapa Sumaúma": "10694",
    "Etapa Ponta Negra": "10695",
}


def extract_competition_id(url: str) -> Optional[str]:
    """Parse the competition ID from a WCA Live URL."""
    url = url.strip().rstrip("/")
    match = re.search(r"/competitions/([^/?#]+)", url)
    if match:
        return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]+", url):
        return url
    return None


def fetch_competition(competition_id: str) -> Optional[dict]:
    """
    Query WCA Live GraphQL API for competition results.
    Returns the competition dict or None on any failure.
    """
    try:
        response = requests.post(
            _API_URL,
            json={"query": _QUERY, "variables": {"id": competition_id}},
            headers=_HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("competition")
    except Exception:
        return None


def fetch_all_circuit_stages() -> dict:
    """
    Fetch results for all circuit stages.
    Returns a dict: { stage_name: competition_data | None }
    """
    results = {}
    for stage_name, comp_id in CIRCUIT_COMPETITIONS.items():
        results[stage_name] = fetch_competition(comp_id)
    return results
