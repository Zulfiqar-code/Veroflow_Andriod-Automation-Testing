# Testing methodology

VeroFlow is *aligned with* ISO/IEC/IEEE 29119 (it does not claim compliance).

| Standard part | How it is used |
|---|---|
| 29119-2 (processes) | Test case -> execute -> compare actual vs expected -> verdict, with evidence stored per run |
| 29119-3 (documentation) | Test cases carry ID, goal/steps, test data, precondition and expected results (`backend/test_cases.json`) |
| 29119-4 (techniques) | Equivalence partitioning and boundary value analysis for input fields; error guessing for negative tests (wrong password, malformed email) |
| 29119-5 (keyword-driven) | Script mode steps (tap, type, verify, scroll) are keywords |

ISO/IEC 25010: only *functional suitability* is tested.

## Known limitations
- `verify` checks text presence only.
- Expected-result items that are not double-quoted exact text are judged by an LLM and are less reliable.
- Goal-mode runs can differ between executions because the planner is an LLM.
- Each step can cost LLM calls (API quota).
- There is no formal accuracy figure yet; measure it with repeated runs and negative tests (false-pass rate).
