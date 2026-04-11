import os
import shutil
import json

LOG_FILE = "/storage/emulated/0/undo_log.json"

def undo_moves():
    if not os.path.exists(LOG_FILE):
        print("No undo log found.")
        return

    with open(LOG_FILE, "r") as f:
        log_data = json.load(f)

    restored = 0

    # Reverse order (important)
    for entry in reversed(log_data):
        src = entry["to"]
        dest = entry["from"]

        try:
            # Create original folder if missing
            os.makedirs(os.path.dirname(dest), exist_ok=True)

            shutil.move(src, dest)
            restored += 1
        except Exception as e:
            pass

    print(f"Restored {restored} files")

    # Clear log after undo
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

if __name__ == "__main__":
    undo_moves()
