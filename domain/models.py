from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RoundResult:
    stage: Optional[str]
    event: str
    round_label: str
    competitor_id: str
    competitor_name: str
    position: int
    total_competitors: int
    points: float
