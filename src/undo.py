import json
import os
import shutil

HISTORY_PATH = "history.json"


# -------------------------
# LOAD / SAVE
# -------------------------
def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_history(data):
    with open(HISTORY_PATH, "w") as f:
        json.dump(data, f, indent=2)


# -------------------------
# UNDO ENGINE
# -------------------------
class UndoEngine:

    # -------------------------
    # CORE REVERSE
    # -------------------------
    def _reverse(self, action):
        try:
            if action.get("operation") == "move":

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
                else:
                    print("File missing:", src)

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
    # SESSION UNDO
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

        target = []
        remaining = []

        for h in history:
            if h.get("session") == last_session:
                target.append(h)
            else:
                remaining.append(h)

        if not target:
            print("Session not found:", last_session)
            return

        for action in reversed(target):
            self._reverse(action)

        save_history(remaining)

        print(f"Session undo completed: {last_session}")
        print(f"Reversed actions: {len(target)}")


# -------------------------
# RUN (USER CONTROL)
# -------------------------
if __name__ == "__main__":
    engine = UndoEngine()

    print("\nChoose Undo Option:")
    print("1. Undo last file")
    print("2. Undo last N files")
    print("3. Undo by folder")
    print("4. Undo last session")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        engine.undo_last()

    elif choice == "2":
        try:
            n = int(input("Enter number of files: "))
            engine.undo_last_n(n)
        except:
            print("Invalid number")

    elif choice == "3":
        folder = input("Enter folder name (e.g. Images): ")
        engine.undo_by_folder(folder)

    elif choice == "4":
        engine.undo_last_session()

    else:
        print("Invalid choice")
