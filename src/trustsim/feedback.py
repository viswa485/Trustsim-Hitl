"""Feedback persistence and transparent feedback-based calibration."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import numpy as np

from trustsim.agents import RuleBasedAgent, ScriptedExpertProxy
from trustsim.envs.road_safety import RoadSafetyEnv
from trustsim.models import Action, FeedbackRecord, Scenario


class FeedbackCalibrator:
    """Interpretable OLS calibration baseline, not a human-preference model."""

    def __init__(self) -> None:
        self.coefficients: np.ndarray | None = None
        self.n_records = 0
        self.sources: set[str] = set()

    def fit(self, records: Iterable[FeedbackRecord]) -> "FeedbackCalibrator":
        rows = list(records)
        if not rows:
            raise ValueError("At least one feedback record is required")
        x = np.asarray(
            [[1.0, 1.0 - row.road_friction, 1.0 - row.visibility] for row in rows],
            dtype=float,
        )
        y = np.asarray([row.recommended_buffer_m for row in rows], dtype=float)
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
            raise ValueError("Feedback records contain non-finite values")
        self.coefficients, *_ = np.linalg.lstsq(x, y, rcond=None)
        self.n_records = len(rows)
        self.sources = {row.source for row in rows}
        return self

    def predict_buffer(self, road_friction: float, visibility: float) -> float:
        if self.coefficients is None:
            raise RuntimeError("Call fit(records) before predict_buffer()")
        features = np.asarray([1.0, 1.0 - road_friction, 1.0 - visibility])
        return max(0.0, float(features @ self.coefficients))

    def metadata(self) -> dict[str, object]:
        return {
            "method": "ordinary_least_squares_linear_calibration",
            "n_records": self.n_records,
            "sources": sorted(self.sources),
            "coefficients": (
                self.coefficients.tolist() if self.coefficients is not None else None
            ),
        }


def collect_proxy_feedback(
    scenarios: Iterable[Scenario],
    expert: ScriptedExpertProxy | None = None,
) -> list[FeedbackRecord]:
    """Collect synthetic proxy labels on a separate calibration scenario stream."""
    expert = expert or ScriptedExpertProxy()
    records: list[FeedbackRecord] = []
    for scenario in scenarios:
        env = RoadSafetyEnv()
        observation = env.reset(scenario)
        agent = RuleBasedAgent()
        while True:
            proposed = agent.act(observation)
            if expert.should_intervene(observation, proposed):
                records.append(
                    FeedbackRecord(
                        scenario_id=scenario.scenario_id,
                        step_index=observation.step_index,
                        road_friction=observation.road_friction,
                        visibility=observation.visibility,
                        gap_m=observation.gap_m,
                        required_gap_m=observation.required_gap_m,
                        proposed_action=int(proposed),
                        corrected_action=int(Action.BRAKE),
                        recommended_buffer_m=expert.recommended_buffer(observation),
                        source="synthetic_expert_proxy",
                        reason="scripted threshold rule requested earlier braking",
                    )
                )
            result = env.step(proposed)
            observation = result.observation
            if result.terminated or result.truncated:
                break
    return records


def write_feedback_jsonl(records: Iterable[FeedbackRecord], path: str | Path) -> int:
    """Write feedback records to a caller-selected safe destination."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with destination.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
            count += 1
    return count


def load_feedback_jsonl(path: str | Path) -> list[FeedbackRecord]:
    records: list[FeedbackRecord] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(FeedbackRecord.from_dict(json.loads(line)))
            except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
                raise ValueError(f"Invalid feedback record on line {line_number}: {exc}") from exc
    return records
