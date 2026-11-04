"""Command-line interface for reproducible experiments."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from trustsim.experiment import run_experiment


def _write_outputs(output_dir: Path, summary: dict, episodes: list) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    rows = [episode.to_dict() for episode in episodes]
    if rows:
        with (output_dir / "episodes.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def _run_command(args: argparse.Namespace) -> int:
    result = run_experiment(episodes=args.episodes, seed=args.seed)
    output_dir = Path(args.output_dir)
    _write_outputs(output_dir, result.summary, result.episodes)
    print(f"TrustSim-HITL experiment complete: {args.episodes} scenarios per condition")
    print(f"Feedback provenance: {result.summary['feedback_source']}")
    print("Condition                 Collision   Unsafe steps   Completion")
    for name, metrics in result.summary["conditions"].items():
        print(
            f"{name:25s} {metrics['collision_rate']:9.3f}"
            f" {metrics['unsafe_step_rate']:14.3f}"
            f" {metrics['episode_completion_rate']:12.3f}"
        )
    print(f"\nWrote {output_dir / 'summary.json'} and {output_dir / 'episodes.csv'}")
    print("Reminder: toy-simulation results are not real-world safety evidence.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trustsim",
        description="Research prototype for autonomous-mobility safety evaluation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="run paired three-condition experiment")
    run_parser.add_argument("--episodes", type=int, default=100)
    run_parser.add_argument("--seed", type=int, default=2026)
    run_parser.add_argument("--output-dir", default="results/local-run")
    run_parser.set_defaults(func=_run_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
