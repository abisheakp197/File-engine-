import json
import os

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []  # ✅ prevents crash if file is empty/corrupt
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def add_entry(entry):
    history = load_history()
    history.append(entry)
    save_history(history)
