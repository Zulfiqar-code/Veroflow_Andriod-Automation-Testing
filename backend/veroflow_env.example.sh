# Copy to veroflow_env.sh (git-ignored), fill in your key, then:  source veroflow_env.sh
export VEROFLOW_API_KEY="PUT_YOUR_KEY_HERE"      # never commit the real key
export VEROFLOW_MODEL="gemini-3.5-flash-lite"    # use a model your key can access
export VEROFLOW_MODE="agent"                     # agent = script mode; test cases with `Expected:` or TC-IDs switch to goal mode
export VEROFLOW_MAX_STEPS=40                     # goal mode step limit
export VEROFLOW_TEST_DATA="test_data.json"       # values the agent may type
export VEROFLOW_TEST_CASES="test_cases.json"     # test case library (TC-01 ...)
# export VEROFLOW_NO_RESET=1                     # keep app data between runs
# export VEROFLOW_NO_IDLE_WAIT=1                 # for apps with endless animations
