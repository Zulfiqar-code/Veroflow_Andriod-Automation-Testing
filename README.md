# VeroFlow – Android Automation Testing

AI-assisted Android UI test automation built on Appium (UiAutomator2) with a FastAPI backend and a Next.js dashboard.

- **Script mode**: step-by-step instructions are executed by an agent that resolves each target on screen.
- **Goal mode**: a test case (goal + expected result) is planned and executed by an LLM-driven plan -> act -> observe loop, then the final screen is checked against the expected results.
- **Screen memory**: CLIP embeddings stored in ChromaDB recognise previously seen screens.
- **Run metrics**: each run writes `metrics.json` computed from its own evidence (verdict, assertion pass rate, steps executed, planner calls, memory hit rate).

See `docs/RUN_VEROFLOW.md` for setup and run instructions.
