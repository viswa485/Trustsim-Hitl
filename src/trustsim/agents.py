"""Baseline and scripted-supervision policies."""
from __future__ import annotations

from dataclasses import dataclass

from trustsim.models import Action, Observation


@dataclass(slots=True)
class RuleBasedAgent:
    """Transparent baseline controller with a configurable extra gap."""

    safety_buffer_m: float = 0.0

    def act(self, observation: Observation) -> Action:
        threshold = observation.required_gap_m + self.safety_buffer_m
        if observation.gap_m <= threshold:
            return Action.BRAKE
        if (
            observation.gap_m > threshold + 18.0
            and observation.ego_speed_mps < observation.lead_speed_mps - 1.0
        ):
            return Action.ACCELERATE
        return Action.COAST


@dataclass(slots=True)
class ScriptedExpertProxy:
    """Deterministic software proxy; not a human or validated safety monitor."""

    base_intervention_margin_m: float = 1.5

    def recommended_buffer(self, observation: Observation) -> float:
        return max(
            0.0,
            self.base_intervention_margin_m
            + 3.0 * (1.0 - observation.road_friction)
            + 2.0 * (1.0 - observation.visibility),
        )

    def should_intervene(self, observation: Observation, proposed: Action) -> bool:
        if proposed == Action.BRAKE:
            return False
        threshold = observation.required_gap_m + self.recommended_buffer(observation)
        return observation.gap_m < threshold
