"""Seeded scenario generation for repeatable experiments."""
from __future__ import annotations

import random

from trustsim.models import Scenario


def generate_scenarios(count: int, seed: int, prefix: str = "eval") -> list[Scenario]:
    """Generate toy scenarios; distributions are not calibrated traffic models."""
    if count <= 0:
        raise ValueError("count must be positive")
    rng = random.Random(seed)
    scenarios: list[Scenario] = []
    for index in range(count):
        initial_speed = rng.uniform(8.0, 20.0)
        lead_speed = rng.uniform(5.0, 19.0)
        gap = rng.uniform(24.0, 65.0)
        friction = rng.uniform(0.35, 1.0)
        visibility = rng.uniform(0.30, 1.0)
        brake_step = rng.choice([None, None, rng.randint(5, 35)])
        brake_decel = rng.uniform(1.5, 4.0) if brake_step is not None else 0.0
        scenarios.append(
            Scenario(
                scenario_id=f"{prefix}-{index:04d}",
                initial_speed_mps=initial_speed,
                lead_speed_mps=lead_speed,
                initial_gap_m=gap,
                road_friction=friction,
                visibility=visibility,
                lead_brake_step=brake_step,
                lead_brake_deceleration_mps2=brake_decel,
            )
        )
    return scenarios
