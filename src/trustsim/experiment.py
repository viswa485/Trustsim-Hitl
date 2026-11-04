"""Paired three-condition experiment runner."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from trustsim.agents import RuleBasedAgent, ScriptedExpertProxy
from trustsim.envs.road_safety import RoadSafetyEnv
from trustsim.feedback import FeedbackCalibrator, collect_proxy_feedback
from trustsim.metrics import EpisodeMetrics, aggregate_metrics
from trustsim.models import Action, Scenario
from trustsim.scenarios import generate_scenarios


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    summary: dict[str, Any]
    episodes: list[EpisodeMetrics]


def _run_episode(
    scenario: Scenario,
    condition: str,
    expert: ScriptedExpertProxy,
    calibrator: FeedbackCalibrator | None = None,
) -> EpisodeMetrics:
    env = RoadSafetyEnv()
    observation = env.reset(scenario)
    baseline = RuleBasedAgent()
    collision = False
    unsafe_steps = braking_actions = overrides = steps = 0
    speeds: list[float] = []
    total_return = 0.0

    while True:
        if condition == "feedback_calibrated" and calibrator is not None:
            baseline.safety_buffer_m = calibrator.predict_buffer(
                observation.road_friction, observation.visibility
            )
        else:
            baseline.safety_buffer_m = 0.0
        proposed = baseline.act(observation)
        executed = proposed
        if condition == "scripted_safety_shield" and expert.should_intervene(
            observation, proposed
        ):
            executed = Action.BRAKE
            overrides += 1
        braking_actions += int(executed == Action.BRAKE)
        result = env.step(executed)
        steps += 1
        total_return += result.reward
        unsafe_steps += int(result.info["unsafe"])
        speeds.append(float(result.info["ego_speed_mps"]))
        observation = result.observation
        collision = bool(result.info["collision"])
        if result.terminated or result.truncated:
            completed = bool(result.truncated and not collision)
            break

    return EpisodeMetrics(
        condition=condition,
        scenario_id=scenario.scenario_id,
        collision=collision,
        completed=completed,
        steps=steps,
        unsafe_steps=unsafe_steps,
        braking_actions=braking_actions,
        supervisor_overrides=overrides,
        mean_speed_mps=sum(speeds) / len(speeds) if speeds else 0.0,
        total_return=total_return,
    )


def run_experiment(episodes: int = 100, seed: int = 2026) -> ExperimentResult:
    """Run paired conditions; calibration uses synthetic proxy labels only."""
    if episodes <= 0:
        raise ValueError("episodes must be positive")
    evaluation_scenarios = generate_scenarios(episodes, seed, "eval")
    calibration_scenarios = generate_scenarios(
        max(episodes, 30), seed + 100_003, "calibration"
    )
    expert = ScriptedExpertProxy()
    proxy_records = collect_proxy_feedback(calibration_scenarios, expert)
    if not proxy_records:
        raise RuntimeError("Calibration generated no proxy feedback; review scenario design")
    calibrator = FeedbackCalibrator().fit(proxy_records)
    conditions = (
        "autonomous_baseline", "scripted_safety_shield", "feedback_calibrated"
    )
    all_episodes: list[EpisodeMetrics] = []
    summaries: dict[str, dict[str, float | int]] = {}
    for condition in conditions:
        rows = [
            _run_episode(
                scenario, condition, expert,
                calibrator if condition == "feedback_calibrated" else None,
            )
            for scenario in evaluation_scenarios
        ]
        all_episodes.extend(rows)
        summaries[condition] = aggregate_metrics(rows)

    summary = {
        "project": "TrustSim-HITL",
        "experiment_version": "0.1.0",
        "seed": seed,
        "evaluation_episodes_per_condition": episodes,
        "paired_evaluation_scenarios": True,
        "calibration_scenarios": len(calibration_scenarios),
        "feedback_source": "synthetic_expert_proxy",
        "feedback_records": len(proxy_records),
        "human_subject_data_used": False,
        "safety_statement": "Toy simulation results are not evidence of real-world vehicle safety.",
        "calibrator": calibrator.metadata(),
        "conditions": summaries,
    }
    return ExperimentResult(summary=summary, episodes=all_episodes)
