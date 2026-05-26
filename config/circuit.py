import json
from dataclasses import dataclass
from pathlib import Path


_DEFAULT_CONFIG_PATH = Path(__file__).with_name("circuit.json")


@dataclass(frozen=True)
class CircuitStage:
    name: str
    competition_id: str


@dataclass(frozen=True)
class CircuitConfig:
    slug: str
    title: str
    stages: tuple[CircuitStage, ...]


def load_circuit_config(path: Path = _DEFAULT_CONFIG_PATH) -> CircuitConfig:
    """Load the circuit definition from a JSON config file."""
    with path.open(encoding="utf-8") as fp:
        raw = json.load(fp)

    stages = tuple(
        CircuitStage(
            name=item["name"],
            competition_id=str(item["competition_id"]),
        )
        for item in raw.get("stages", [])
    )
    if not stages:
        raise ValueError("Circuit config must define at least one stage.")

    return CircuitConfig(
        slug=raw.get("slug", "Circuito"),
        title=raw.get("title", "Ranking do Circuito"),
        stages=stages,
    )


def stages_as_mapping(config: CircuitConfig) -> dict[str, str]:
    """Return the legacy {stage_name: competition_id} mapping."""
    return {stage.name: stage.competition_id for stage in config.stages}
