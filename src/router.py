import os
import shutil
from logger import log_event


class FileRouter:

    # -------------------------
    # SINGLE FILE MOVE
    # -------------------------
    def move_file(self, src, dst, session_id=None):
        if not os.path.exists(src):
            print("Source not found:", src)
            return False

        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)

            shutil.move(src, dst)

            # log event with session support
            log_event("MOVE", src, dst, session_id)

            print(f"Moved: {src} -> {dst}")
            return True

        except Exception as e:
            print("Move failed:", e)
            return False

    # -------------------------
    # BATCH MOVE
    # -------------------------
    def move_files(self, file_list, folder_name, session_id=None):
        if not file_list:
            print("No files to move")
            return

        base_path = f"/storage/emulated/0/{folder_name}"
        os.makedirs(base_path, exist_ok=True)

        moved = 0

        for file in file_list:
            try:
                src = file["path"]
                filename = os.path.basename(src)
                dst = os.path.join(base_path, filename)

                success = self.move_file(src, dst, session_id)

                if success:
                    moved += 1

            except Exception as e:
                print("Batch error:", e)

        print(f"Batch complete: {moved}/{len(file_list)} moved")
