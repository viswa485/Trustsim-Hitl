from trustsim.envs.road_safety import RoadSafetyEnv
from trustsim.models import Action, Scenario


def make_scenario(**overrides):
    values = dict(
        scenario_id="test-0001",
        initial_speed_mps=12.0,
        lead_speed_mps=10.0,
        initial_gap_m=40.0,
        road_friction=0.8,
        visibility=0.9,
        lead_brake_step=5,
        lead_brake_deceleration_mps2=3.0,
        max_steps=20,
    )
    values.update(overrides)
    return Scenario(**values)


def test_reset_sets_initial_state():
    obs = RoadSafetyEnv().reset(make_scenario())
    assert obs.ego_speed_mps == 12.0
    assert obs.gap_m == 40.0
    assert obs.required_gap_m > 0


def test_braking_reduces_ego_speed():
    env = RoadSafetyEnv()
    env.reset(make_scenario())
    assert env.step(Action.BRAKE).observation.ego_speed_mps < 12.0


def test_environment_requires_reset():
    try:
        RoadSafetyEnv().observe()
    except RuntimeError as exc:
        assert "reset" in str(exc)
    else:
        raise AssertionError("observe() should require reset()")
