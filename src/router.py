import os
import time
import shutil
from logger import log_event
from history import add_entry


class FileRouter:

    # -------------------------
    # SINGLE FILE MOVE (silent core)
    # -------------------------
    def move_file(self, src, dst, session_id=None):

        if not os.path.exists(src):
            return False

        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)

            log_event("MOVE", src, dst, session_id)

            add_entry({
                "from": src,
                "to": dst,
                "operation": "move",
                "session": session_id
            })

            return True

        except Exception:
            return False

    # -------------------------
    # STREAM MOVE WITH LIVE PROGRESS
    # -------------------------
    def move_files(self, file_list, folder_name, session_id=None):

        if not file_list:
            print(f"No files to move for {folder_name}", flush=True)
            return

        base_path = f"/storage/emulated/0/{folder_name}"
        os.makedirs(base_path, exist_ok=True)

        total = len(file_list)
        moved = 0

        start_time = time.time()

        print(f"\n--- Moving {folder_name} ({total}) ---\n", flush=True)

        for i, file in enumerate(file_list, start=1):

            try:
                src = file["path"]
                filename = os.path.basename(src)
                dst = os.path.join(base_path, filename)

                success = self.move_file(src, dst, session_id)

                if success:
                    moved += 1

                # -------------------------
                # LIVE SPEED + PROGRESS
                # -------------------------
                elapsed = time.time() - start_time
                speed = i / elapsed if elapsed > 0 else 0

                print(
                    f"[{i}/{total}] moved={moved} speed={speed:.2f} files/sec",
                    flush=True
                )

            except Exception as e:
                print(f"Batch error: {e}", flush=True)

        print(
            f"\nBatch complete: {moved}/{total} ({folder_name})",
            flush=True
        )
