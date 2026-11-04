from trustsim.feedback import FeedbackCalibrator, collect_proxy_feedback
from trustsim.scenarios import generate_scenarios


def test_proxy_feedback_keeps_source_label():
    rows = collect_proxy_feedback(generate_scenarios(20, 91, "cal"))
    assert rows
    assert {row.source for row in rows} == {"synthetic_expert_proxy"}


def test_calibrator_predicts_nonnegative_margin():
    rows = collect_proxy_feedback(generate_scenarios(20, 92, "cal"))
    model = FeedbackCalibrator().fit(rows)
    assert model.predict_buffer(0.5, 0.5) >= 0
