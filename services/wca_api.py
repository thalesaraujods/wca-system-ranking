import re
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.circuit import load_circuit_config, stages_as_mapping

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
          person {
            name
          }
        }
      }
    }
  }
}
"""

# Legacy mapping used by the UI. Source of truth is config/circuit.json.
CIRCUIT_COMPETITIONS = stages_as_mapping(load_circuit_config())


def _build_session() -> requests.Session:
    session = requests.Session()
    try:
        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
    except TypeError:
        # Some hosted environments pin older urllib3 versions. A plain session is
        # better than failing before the request can be attempted.
        pass
    return session


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
        response = _build_session().post(
            _API_URL,
            json={"query": _QUERY, "variables": {"id": competition_id}},
            headers=_HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            return None
        return data.get("data", {}).get("competition")
    except Exception:
        return None


def fetch_all_circuit_stages(
    competitions: Optional[dict[str, str]] = None,
) -> dict:
    """
    Fetch results for all circuit stages.
    Returns a dict: { stage_name: competition_data | None }
    """
    competitions = competitions or CIRCUIT_COMPETITIONS
    results = {}
    for stage_name, comp_id in competitions.items():
        results[stage_name] = fetch_competition(comp_id)
    return results
