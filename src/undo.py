import json
import os
import shutil

HISTORY_PATH = "../storage/history/history.json"


def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []

    with open(HISTORY_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_history(data):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(data, f, indent=2)


class UndoEngine:

    # -------------------------
    # CORE REVERSE
    # -------------------------
    def _reverse(self, action):
        try:
            if action.get("action") == "MOVE":
                src = action.get("to")
                dst = action.get("from")

                if not src or not dst:
                    return

                src = os.path.normpath(src)
                dst = os.path.normpath(dst)

                if os.path.exists(src):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.move(src, dst)
                    print(f"UNDO MOVE: {src} -> {dst}")

        except Exception as e:
            print("Undo error:", e)

    # -------------------------
    # UNDO LAST ACTION
    # -------------------------
    def undo_last(self):
        history = load_history()

        if not history:
            print("Nothing to undo")
            return

        last = history.pop()
        self._reverse(last)

        save_history(history)

    # -------------------------
    # UNDO LAST N ACTIONS
    # -------------------------
    def undo_last_n(self, n=5):
        history = load_history()

        if not history:
            print("Nothing to undo")
            return

        count = 0

        while history and count < n:
            action = history.pop()
            self._reverse(action)
            count += 1

        save_history(history)
        print(f"Undo completed: {count} actions")

    # -------------------------
    # UNDO BY FOLDER
    # -------------------------
    def undo_by_folder(self, folder_name):
        history = load_history()

        target = []
        remaining = []

        for h in history:
            if folder_name in (h.get("to") or ""):
                target.append(h)
            else:
                remaining.append(h)

        if not target:
            print("No actions found for folder:", folder_name)
            return

        for action in reversed(target):
            self._reverse(action)

        save_history(remaining)

        print(f"Undo folder '{folder_name}' completed: {len(target)} actions")

    # -------------------------
    # 🔥 NEW: SESSION UNDO (FULL RUN ROLLBACK)
    # -------------------------
    def undo_last_session(self):
        history = load_history()

        if not history:
            print("Nothing to undo")
            return

        last_session = history[-1].get("session")

        if not last_session:
            print("No session data found")
            return

        remaining = []
        target = []

        # collect session actions
        for h in history:
            if h.get("session") == last_session:
                target.append(h)
            else:
                remaining.append(h)

        if not target:
            print("Session not found:", last_session)
            return

        # reverse in correct order
        for action in reversed(target):
            self._reverse(action)

        save_history(remaining)

        print(f"Session undo completed: {last_session}")
        print(f"Reversed actions: {len(target)}")
