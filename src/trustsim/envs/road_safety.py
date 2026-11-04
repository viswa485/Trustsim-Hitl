"""Deliberately simplified longitudinal-road simulation; not vehicle dynamics."""
from __future__ import annotations

from trustsim.models import Action, Observation, Scenario, StepResult


class RoadSafetyEnv:
    """Toy environment omitting steering, road geometry and sensor noise."""

    dt_s = 0.5
    max_speed_mps = 30.0
    base_reaction_time_s = 1.0
    base_gap_margin_m = 3.0
    max_braking_deceleration_mps2 = 6.0

    def __init__(self) -> None:
        self.scenario: Scenario | None = None
        self.ego_speed_mps = 0.0
        self.lead_speed_mps = 0.0
        self.gap_m = 0.0
        self.step_index = 0
        self.collision = False

    def reset(self, scenario: Scenario) -> Observation:
        self.scenario = scenario
        self.ego_speed_mps = scenario.initial_speed_mps
        self.lead_speed_mps = scenario.lead_speed_mps
        self.gap_m = scenario.initial_gap_m
        self.step_index = 0
        self.collision = False
        return self.observe()

    def observe(self) -> Observation:
        self._require_scenario()
        assert self.scenario is not None
        closing_speed = max(0.0, self.ego_speed_mps - self.lead_speed_mps)
        reaction_time = self.base_reaction_time_s + (1.0 - self.scenario.visibility) * 1.25
        deceleration = max(
            1.0, self.max_braking_deceleration_mps2 * self.scenario.road_friction
        )
        required_gap = (
            self.base_gap_margin_m
            + self.ego_speed_mps * reaction_time
            + closing_speed**2 / (2.0 * deceleration)
        )
        ttc = min(60.0, self.gap_m / closing_speed) if closing_speed > 1e-6 else 60.0
        return Observation(
            self.ego_speed_mps, self.lead_speed_mps, max(0.0, self.gap_m),
            self.scenario.road_friction, self.scenario.visibility,
            required_gap, ttc, self.step_index,
        )

    def step(self, action: Action | int) -> StepResult:
        self._require_scenario()
        assert self.scenario is not None
        action = Action(int(action))
        scenario = self.scenario
        if scenario.lead_brake_step is not None and self.step_index >= scenario.lead_brake_step:
            self.lead_speed_mps = max(
                0.0,
                self.lead_speed_mps - scenario.lead_brake_deceleration_mps2 * self.dt_s,
            )
        if action == Action.ACCELERATE:
            acceleration = 1.2
        elif action == Action.BRAKE:
            acceleration = -self.max_braking_deceleration_mps2 * scenario.road_friction
        else:
            acceleration = -0.15
        previous_speed = self.ego_speed_mps
        self.ego_speed_mps = min(
            self.max_speed_mps,
            max(0.0, self.ego_speed_mps + acceleration * self.dt_s),
        )
        average_speed = (previous_speed + self.ego_speed_mps) / 2.0
        self.gap_m += (self.lead_speed_mps - average_speed) * self.dt_s
        self.step_index += 1
        self.collision = self.gap_m <= 0.0
        observation = self.observe()
        unsafe = observation.gap_m < observation.required_gap_m
        reward = 0.05 * self.ego_speed_mps / self.max_speed_mps
        if unsafe:
            reward -= 0.15
        if self.collision:
            reward -= 10.0
        terminated = self.collision
        truncated = self.step_index >= scenario.max_steps and not terminated
        info = {
            "collision": self.collision, "unsafe": unsafe,
            "required_gap_m": observation.required_gap_m, "gap_m": observation.gap_m,
            "action": int(action), "ego_speed_mps": self.ego_speed_mps,
        }
        return StepResult(observation, reward, terminated, truncated, info)

    def _require_scenario(self) -> None:
        if self.scenario is None:
            raise RuntimeError("Call reset(scenario) before observe() or step()")
