"""Shared data models for TrustSim-HITL."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import IntEnum
from typing import Any


class Action(IntEnum):
    ACCELERATE = 0
    COAST = 1
    BRAKE = 2


@dataclass(frozen=True, slots=True)
class Scenario:
    scenario_id: str
    initial_speed_mps: float
    lead_speed_mps: float
    initial_gap_m: float
    road_friction: float
    visibility: float
    lead_brake_step: int | None
    lead_brake_deceleration_mps2: float
    max_steps: int = 100

    def __post_init__(self) -> None:
        if self.initial_speed_mps < 0 or self.lead_speed_mps < 0:
            raise ValueError("Initial speeds must be non-negative")
        if self.initial_gap_m <= 0:
            raise ValueError("Initial gap must be positive")
        if not 0.1 <= self.road_friction <= 1.0:
            raise ValueError("road_friction must be in [0.1, 1.0]")
        if not 0.1 <= self.visibility <= 1.0:
            raise ValueError("visibility must be in [0.1, 1.0]")
        if self.lead_brake_step is not None and self.lead_brake_step < 0:
            raise ValueError("lead_brake_step must be non-negative or None")
        if self.max_steps <= 0:
            raise ValueError("max_steps must be positive")


@dataclass(frozen=True, slots=True)
class Observation:
    ego_speed_mps: float
    lead_speed_mps: float
    gap_m: float
    road_friction: float
    visibility: float
    required_gap_m: float
    time_to_collision_s: float
    step_index: int

    def as_vector(self) -> list[float]:
        return [
            self.ego_speed_mps, self.lead_speed_mps, self.gap_m,
            self.road_friction, self.visibility, self.time_to_collision_s,
        ]


@dataclass(frozen=True, slots=True)
class StepResult:
    observation: Observation
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, Any]


@dataclass(frozen=True, slots=True)
class FeedbackRecord:
    """Correction record whose source field preserves provenance."""

    scenario_id: str
    step_index: int
    road_friction: float
    visibility: float
    gap_m: float
    required_gap_m: float
    proposed_action: int
    corrected_action: int
    recommended_buffer_m: float
    source: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "FeedbackRecord":
        return cls(**payload)
