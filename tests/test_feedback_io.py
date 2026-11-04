from trustsim.feedback import collect_proxy_feedback, load_feedback_jsonl, write_feedback_jsonl
from trustsim.scenarios import generate_scenarios


def test_feedback_round_trip(tmp_path):
    rows = collect_proxy_feedback(generate_scenarios(5, 778, "io"))
    path = tmp_path / "feedback.jsonl"
    assert write_feedback_jsonl(rows, path) == len(rows)
    assert [x.to_dict() for x in load_feedback_jsonl(path)] == [x.to_dict() for x in rows]
