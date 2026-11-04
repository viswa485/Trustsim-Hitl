from trustsim.experiment import run_experiment


def test_experiment_uses_paired_scenarios_and_three_conditions():
    result = run_experiment(episodes=8, seed=123)
    assert result.summary["human_subject_data_used"] is False
    assert result.summary["feedback_source"] == "synthetic_expert_proxy"
    assert set(result.summary["conditions"]) == {
        "autonomous_baseline",
        "scripted_safety_shield",
        "feedback_calibrated",
    }
    assert len(result.episodes) == 24
    assert len({row.scenario_id for row in result.episodes}) == 8
