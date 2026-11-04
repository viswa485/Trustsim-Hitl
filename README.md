# TrustSim-HITL

**A research prototype for evaluating human-supervised safety interventions in autonomous mobility simulations.**

[![CI](https://github.com/viswa485/Trustsim-Hitl/actions/workflows/ci.yml/badge.svg)](https://github.com/viswa485/Trustsim-Hitl/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Research status:** early-stage, actively developing prototype. The current implementation is a lightweight, deterministic Python simulation and evaluation harness. It is **not** a validated autonomous-driving system, a safety certification artefact, a completed VR environment, or evidence from human-subject experiments.

## Research question

How do different supervision strategies affect safety-related outcomes and task performance in a controlled autonomous-mobility simulation, and how can structured human corrections be incorporated into subsequent policy calibration?

TrustSim-HITL is designed to grow from a reproducible Python baseline into a simulation-backed research demonstrator. It separates the simulation interface, agent policy, safety supervisor, feedback records and experiment runner so that a CARLA/Unreal or Unity front end can be added without rewriting the evaluation core.

## What is implemented now

- A small, deterministic longitudinal-road simulation with configurable lead-vehicle braking, road friction and visibility.
- A transparent rule-based driving policy.
- A **scripted expert proxy** that can override unsafe proposed actions. This proxy is not a human participant.
- A feedback-record schema and a simple linear calibration model. The initial reproducible experiment calibrates from **synthetic expert-proxy feedback**, not real human data.
- A three-condition experiment runner: autonomous baseline, baseline plus safety shield, and feedback-calibrated policy.
- Episode-level CSV output and a JSON summary with safety and task-performance metrics.
- Unit tests and continuous integration.
- An optional Gymnasium adapter is included in source; it has not yet been runtime-verified in this environment because Gymnasium is not installed.

## Planned, not yet implemented

- A real-time human feedback interface and human-participant data collection.
- CARLA integration and scenario import/export.
- Unreal Engine / Unity visualisation and VR interaction.
- ROS 2 integration and robotics/autonomous-stack connectivity.
- Learning-based policies (for example PPO via Stable-Baselines3) and statistically powered human-AI experiments.

For a supervisor meeting, see [PROFESSOR_BRIEF.md](docs/PROFESSOR_BRIEF.md). GitHub bootstrap instructions are in [GITHUB_SETUP.md](GITHUB_SETUP.md).

See [PROJECT_STATUS.md](docs/PROJECT_STATUS.md), [RESEARCH_PLAN.md](docs/RESEARCH_PLAN.md), [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md), [VR_INTEGRATION_PLAN.md](docs/VR_INTEGRATION_PLAN.md), [CARLA_INTEGRATION_PLAN.md](docs/CARLA_INTEGRATION_PLAN.md) and the clearly qualified [pilot run report](docs/PILOT_RUN_REPORT.md).

## Quick start

Python 3.11 or newer is recommended.

```bash
git clone https://github.com/viswa485/Trustsim-Hitl.git
cd Trustsim-Hitl
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
pytest
```

Run a reproducible experiment:

```bash
trustsim run --episodes 100 --seed 2026 --output-dir results/run-100
```

Or run from a source checkout without installing the console script:

```bash
PYTHONPATH=src python -m trustsim.cli run --episodes 100 --seed 2026 --output-dir results/run-100
```

The command writes `summary.json` and `episodes.csv`. Results are generated locally and are not committed by default. Always retain the seed and configuration when comparing runs.

## Experimental conditions

| Condition | Policy | Interpretation |
|---|---|---|
| `autonomous_baseline` | Rule-based policy | No external intervention |
| `scripted_safety_shield` | Baseline plus scripted expert proxy | A deterministic software supervisor overrides selected actions; **not** a human-in-the-loop condition |
| `feedback_calibrated` | Baseline with a calibration model fitted to proxy feedback | Tests the feedback-data pipeline using synthetic proxy labels; **not** evidence of human learning |

All conditions use the same evaluation scenarios for paired comparison. Calibration scenarios are generated from a separate seed stream to reduce evaluation leakage.

## Metrics

The current runner reports collision rate, unsafe-step rate, episode completion rate, mean speed, braking-action rate, supervisor overrides per episode and mean episode return. Metric definitions and limitations are documented in [METRICS.md](docs/METRICS.md).

No performance claims should be made until results have been run, inspected and reproduced. The simulation is deliberately simplified and must not be used to infer real-world vehicle safety.

## Architecture

```text
Scenario generator
       |
       v
Road-safety environment ----> Observation / transition log
       |                                  |
       v                                  v
Rule-based policy                  Metric calculation
       |
       +----> scripted safety shield (proxy only)
       |
       +----> feedback-calibrated policy
                    ^
                    |
          feedback record schema
          (synthetic now; human later)

Experiment runner ---> JSON summary + episode CSV

Future adapters: Gymnasium / CARLA / ROS 2 / Unreal / Unity / VR
```

## Open-source ecosystem

TrustSim-HITL is an original research scaffold and does not copy source files from the projects below. They are potential integration points or development dependencies; the current baseline does not require CARLA, ROS 2 or a game engine.

- [CARLA](https://github.com/carla-simulator/carla) — open-source autonomous-driving simulator; a future integration target.
- [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) — standard API for RL environments; optional adapter target.
- [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) — RL algorithms maintained by DLR-RM; optional future training component.
- [CARLA ScenarioRunner](https://github.com/carla-simulator/scenario_runner) — scenario execution for compatible CARLA releases; evaluate version compatibility before integration.
- [CARLA ROS bridge](https://github.com/carla-simulator/ros-bridge) — future ROS 2 connectivity option; verify compatibility with the selected CARLA and ROS releases.

The engine and simulator installation/licensing requirements remain separate from this repository. Unity and Unreal Engine are not treated here as OSI-approved open-source dependencies. See [OPEN_SOURCE_ECOSYSTEM.md](docs/OPEN_SOURCE_ECOSYSTEM.md).

## Safety, ethics and responsible use

- This is research software, not a driving controller or safety assurance case.
- All current experiments are software-generated simulations; the expert is a scripted proxy.
- Do not connect this prototype to a real vehicle or use it for operational decisions.
- Do not claim human-subject results until an appropriately reviewed study has actually been conducted.
- Store no personal or sensitive participant data in the repository. Establish consent, data minimisation, retention and institutional ethics review before recruiting participants.

See [ETHICS_AND_LIMITATIONS.md](docs/ETHICS_AND_LIMITATIONS.md) and [SECURITY.md](SECURITY.md).

## Roadmap

1. **M0 — Reproducible core:** environment, scripted proxy, feedback schema, metrics, tests and experiment runner.
2. **M1 — Research validation:** scenario coverage, repeated seeds, confidence intervals and baseline sensitivity analysis.
3. **M2 — Real human feedback:** instrumented review interface, consented study protocol and anonymised feedback ingestion.
4. **M3 — Simulator integration:** CARLA scenarios and documented version matrix.
5. **M4 — Human-centred demonstrator:** Unreal/Unity visualisation, VR interaction and usability evaluation.
6. **M5 — Learning and robotics:** Gymnasium/SB3 policy experiments and optional ROS 2 bridge.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Research assumptions, scenario definitions and changes to metric semantics should be documented and reviewed like code.

## Citation

A provisional citation file is provided in [CITATION.cff](CITATION.cff). Please cite the repository as software only; it is not a peer-reviewed publication.
