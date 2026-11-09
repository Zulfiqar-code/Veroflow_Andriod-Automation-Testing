# Run metrics

Every run writes `metrics.json` into its run folder. All values are computed from that run's own
evidence (`steps.json`, `goal_result.json`); nothing is typed in by hand.

| Field | Meaning |
|---|---|
| `verdict` | PASSED / FAILED: actual result compared with the expected result of the test case |
| `assertions_total`, `assertions_met`, `assertion_pass_rate` | Expected-result items that were met. This is the metric that reflects test correctness. `null` when there are no assertions |
| `assertions_exact_text`, `assertions_llm_judged` | How many checks were exact text matches vs LLM-judged (the latter are less reliable) |
| `steps_executed`, `steps_passed`, `steps_failed`, `step_pass_rate` | Action-level efficiency, not correctness. In goal mode, failed steps may be recovered attempts |
| `planner_calls` | Goal-mode planning iterations (LLM calls) |
| `steps_resolved_by_llm` | Steps where the LLM chose the target element |
| `screens_recognized`, `screen_memory_hits`, `screen_memory_hit_rate` | Screens recognised from the CLIP + ChromaDB memory |

Step pass rate can be 100% while the verdict is FAILED (the actions ran, but the expected result was not met).
