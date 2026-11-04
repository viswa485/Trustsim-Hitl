"""Optional Gymnasium adapter. Install with pip install -e '.[rl]'."""
from __future__ import annotations

from dataclasses import replace

import numpy as np

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError as exc:  # pragma: no cover
    raise ImportError("Gymnasium is optional; install with: pip install -e '.[rl]'") from exc

from trustsim.envs.road_safety import RoadSafetyEnv
from trustsim.models import Action, Scenario
from trustsim.scenarios import generate_scenarios


class SafeDrivingGymEnv(gym.Env):
    """Gymnasium wrapper around the simplified toy environment."""

    metadata = {"render_modes": []}

    def __init__(self, max_steps: int = 100):
        super().__init__()
        self.max_steps = max_steps
        self.environment = RoadSafetyEnv()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=np.asarray([0, 0, 0, .1, .1, 0], dtype=np.float32),
            high=np.asarray([30, 30, 1000, 1, 1, 60], dtype=np.float32),
            dtype=np.float32,
        )

    def reset(self, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        scenario = options.get("scenario") if options else None
        if not isinstance(scenario, Scenario):
            scenario_seed = int(self.np_random.integers(0, 2**31 - 1))
            scenario = generate_scenarios(1, scenario_seed, "gym")[0]
        scenario = replace(scenario, max_steps=self.max_steps)
        observation = self.environment.reset(scenario)
        return np.asarray(observation.as_vector(), dtype=np.float32), {
            "scenario_id": scenario.scenario_id
        }

    def step(self, action: int):
        result = self.environment.step(Action(int(action)))
        return (
            np.asarray(result.observation.as_vector(), dtype=np.float32),
            float(result.reward), bool(result.terminated), bool(result.truncated), result.info,
        )
