"""Offline unit tests for goal mode helpers (no emulator, no LLM, no network).
Run from the backend folder:  python -m pytest tests -q
"""
import json
import pytest

from pipeline import goal_runner as gr


PLAIN = (
    "Open the app and log in.\n"
    "Test data: email = a@b.com; password = Secret1\n"
    'Expected: "Welcome"; Order is listed'
)


def test_looks_like_test_case_detects_expected_line():
    assert gr.looks_like_test_case(PLAIN)
    assert not gr.looks_like_test_case("tap the login button")


def test_looks_like_test_case_detects_json_goal():
    assert gr.looks_like_test_case('{"goal": "add to cart", "expected": ["Cart"]}')
    assert not gr.looks_like_test_case('{"unrelated": 1}')


def test_parse_plain_format_extracts_goal_data_expected():
    case = gr.parse_test_case(PLAIN)
    assert "log in" in case["goal"].lower()
    assert case["data"]["email"] == "a@b.com"
    assert case["expected"] == ['"Welcome"', "Order is listed"]


def test_value_allowed_blocks_invented_values():
    case = {"goal": "log in", "data": {"email": "a@b.com"}, "setup": ""}
    nodes = [{"text": "Email", "desc": ""}]
    assert gr.value_allowed("a@b.com", case, nodes)        # from test data
    assert gr.value_allowed("Email", case, nodes)          # visible on screen
    assert not gr.value_allowed("made.up@x.com", case, nodes)


def _write(run_dir, steps, goal=None):
    (run_dir / "steps.json").write_text(json.dumps(steps))
    if goal is not None:
        (run_dir / "goal_result.json").write_text(json.dumps(goal))


def test_metrics_goal_mode_counts_assertions_and_memory(tmp_path):
    _write(
        tmp_path,
        [
            {"status": "passed", "screen_source": "memory hit", "decided_by": "exact label match (LLM skipped)"},
            {"status": "failed", "screen_source": "new screen (vision model)", "decided_by": "llm"},
            {"status": "passed", "screen_source": "memory hit", "decided_by": "LLM semantic match"},
        ],
        {"iterations": 3, "checks": [
            {"method": "exact text", "met": True},
            {"method": "LLM judge", "met": False},
        ]},
    )
    m = gr.compute_metrics(str(tmp_path), "goal", "FAILED")
    assert (m["steps_executed"], m["steps_passed"], m["steps_failed"]) == (3, 2, 1)
    assert m["assertion_pass_rate"] == 0.5
    assert (m["assertions_exact_text"], m["assertions_llm_judged"]) == (1, 1)
    assert m["screen_memory_hit_rate"] == pytest.approx(0.667, abs=0.001)
    assert m["steps_resolved_by_llm"] == 2
    assert m["planner_calls"] == 3


def test_metrics_never_exceed_one_hundred_percent(tmp_path):
    _write(tmp_path, [{"status": "passed"}] * 4, {"checks": []})
    m = gr.compute_metrics(str(tmp_path), "goal", "PASSED")
    assert m["step_pass_rate"] == 1.0
    assert m["assertion_pass_rate"] is None     # no assertions -> no rate, not a fake 100%


def test_metrics_missing_files_do_not_crash(tmp_path):
    m = gr.compute_metrics(str(tmp_path / "nope"), "script", "FAILED")
    assert m["steps_executed"] == 0 and m["step_pass_rate"] is None
