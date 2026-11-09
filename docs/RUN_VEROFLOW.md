# VeroFlow: how to run it on a new laptop (Ubuntu/Linux)

Four things must be running together: emulator, Appium, backend, dashboard.
Do not put your real API key in this file or commit it to git.

## 0. One-time setup

```bash
# Android SDK + an emulator (create an AVD in Android Studio > Device Manager), then:
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator

# Node.js 18+ and Appium
npm install -g appium
appium driver install uiautomator2

# Python backend
cd ~/Documents/veroflow/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt        # fastapi, uvicorn, python-multipart, appium-python-client, open_clip, chromadb ...

# Dashboard
cd ~/Documents/veroflow/veroflow-dashboard
npm install
```

## 1. Config file (API key lives here)

Create `~/Documents/veroflow/backend/veroflow_env.sh`:

```bash
export VEROFLOW_MODE=agent
export VEROFLOW_LLM=openai
export VEROFLOW_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export VEROFLOW_API_KEY="PUT_YOUR_KEY_HERE"
export VEROFLOW_MODEL="gemini-2.5-flash"
export VEROFLOW_MAX_TOKENS=8000
```

Keep it out of git:

```bash
echo veroflow_env.sh >> ~/Documents/veroflow/.gitignore
```

## 2. Every time you run (4 terminals)

Terminal 1, emulator (or start it from Android Studio):
```bash
emulator -list-avds
emulator -avd <AVD_NAME>
adb devices                      # must show: emulator-5554   device
adb -s emulator-5554 shell settings put secure stylus_handwriting_enabled 0   # stops the "Try out your stylus" popup
```

Terminal 2, Appium:
```bash
appium
```

Terminal 3, backend:
```bash
cd ~/Documents/veroflow/backend
source venv/bin/activate
source veroflow_env.sh
python -m uvicorn main:app --reload --port 8000
```

Terminal 4, dashboard (open http://localhost:3000):
```bash
cd ~/Documents/veroflow/veroflow-dashboard
npm run dev
```

Before each run: put the app in a fresh state (the test installs the APK; do not touch the emulator while it runs).

## 3. Change the API key / model

```bash
cd ~/Documents/veroflow/backend

# show the current settings (key is cut to 6 characters)
grep -n "VEROFLOW_" veroflow_env.sh | sed 's/\(API_KEY="\?.\{6\}\).*/\1.../'

# replace the key
sed -i 's|^export VEROFLOW_API_KEY=.*|export VEROFLOW_API_KEY="NEW_KEY_HERE"|' veroflow_env.sh

# replace the model
sed -i 's|^export VEROFLOW_MODEL=.*|export VEROFLOW_MODEL="gemini-2.5-flash-lite"|' veroflow_env.sh

# find every other place that still mentions an old provider
grep -rniE "ollama|llama|11434" --include=*.py .
```

Then restart the backend (Ctrl+C in terminal 3, run the 3 commands again).

## 4. Quick checks

```bash
curl -s http://127.0.0.1:4723/status | head -c 200      # Appium alive?
curl -s http://127.0.0.1:8000/docs -o /dev/null -w "%{http_code}\n"   # backend alive? (200)
env | grep VEROFLOW_MODE                                 # must print VEROFLOW_MODE=agent
```

## 5. Common errors

| Error | Meaning / fix |
|---|---|
| `Connection refused ... port 4723` | Appium is not running. Start `appium`. |
| `Could not import module "main"` | Run uvicorn from the `backend` folder. |
| `No module named 'fastapi'` | Activate the venv: `source venv/bin/activate`. |
| `command not found` when sourcing the env file | Every line in `veroflow_env.sh` must start with `export`. |
| `HTTP 429 ... exceeded your current quota` | Gemini limit reached. Change `VEROFLOW_MODEL`, use another project's key, or wait for the daily reset. |
| `nothing on screen matches` | The old rule-based runner is active. `VEROFLOW_MODE=agent` is missing. |
| `Visible on screen: []` | A system dialog is on top of the app (see the stylus command above). |
