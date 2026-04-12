import json
import os
import time
import uuid

HISTORY_PATH = "../storage/history/history.json"


def _load():
    if not os.path.exists(HISTORY_PATH):
        return []

    with open(HISTORY_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def _save(data):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(data, f, indent=2)


# -------------------------
# CREATE SESSION ID
# -------------------------
def create_session():
    return str(uuid.uuid4())


# -------------------------
# LOG EVENT WITH SESSION
# -------------------------
def log_event(action, src, dst=None, session_id=None):
    data = _load()

    event = {
        "id": int(time.time() * 1000),
        "session": session_id,
        "action": action,
        "from": src,
        "to": dst,
        "time": time.ctime()
    }

    data.append(event)
    _save(data)
