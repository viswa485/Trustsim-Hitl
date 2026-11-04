"""Metric aggregation for experiment episodes."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class EpisodeMetrics:
    condition: str
    scenario_id: str
    collision: bool
    completed: bool
    steps: int
    unsafe_steps: int
    braking_actions: int
    supervisor_overrides: int
    mean_speed_mps: float
    total_return: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def aggregate_metrics(episodes: Iterable[EpisodeMetrics]) -> dict[str, float | int]:
    rows = list(episodes)
    if not rows:
        raise ValueError("Cannot aggregate an empty episode list")
    total_steps = sum(row.steps for row in rows)
    return {
        "episode_count": len(rows),
        "collision_rate": sum(row.collision for row in rows) / len(rows),
        "unsafe_step_rate": (
            sum(row.unsafe_steps for row in rows) / total_steps
            if total_steps else 0.0
        ),
        "episode_completion_rate": sum(row.completed for row in rows) / len(rows),
        "mean_steps": total_steps / len(rows),
        "mean_speed_mps": sum(row.mean_speed_mps for row in rows) / len(rows),
        "braking_action_rate": (
            sum(row.braking_actions for row in rows) / total_steps
            if total_steps else 0.0
        ),
        "supervisor_overrides_per_episode": (
            sum(row.supervisor_overrides for row in rows) / len(rows)
        ),
        "mean_episode_return": sum(row.total_return for row in rows) / len(rows),
    }
