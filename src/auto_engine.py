import time
from scanner import FileScanner
from filter import FileFilter
from router import FileRouter
from logger import create_session
from undo import UndoEngine


class AutoEngine:

    def __init__(self, path="/storage/emulated/0"):
        self.path = path
        self.router = FileRouter()
        self.undo = UndoEngine()

    # -------------------------
    # SAFETY CHECK
    # -------------------------
    def is_safe(self, file_path):
        unsafe_keywords = [
            "Android/data",
            "Android/obb",
            ".system",
            "com.android"
        ]

        for k in unsafe_keywords:
            if k in file_path:
                return False
        return True

    # -------------------------
    # RUN ENGINE
    # -------------------------
    def run_once(self):
        session_id = create_session()
        print("\n[AUTO SESSION]", session_id)

        scanner = FileScanner(self.path)
        files = scanner.scan()

        file_filter = FileFilter(files)

        images = file_filter.images()
        large_files = file_filter.by_size(min_size=10)

        # filter safe files only
        safe_images = [f for f in images if self.is_safe(f["path"])]
        safe_large = [f for f in large_files if self.is_safe(f["path"])]

        print("Safe images:", len(safe_images))
        print("Safe large files:", len(safe_large))

        # execute automation
        self.router.move_files(safe_images[:5], "Images", session_id)
        self.router.move_files(safe_large[:3], "LargeFiles", session_id)

        print("Auto run completed.")

    # -------------------------
    # LOOP MODE (AUTONOMOUS)
    # -------------------------
    def start(self, interval=60):
        print("AUTONOMOUS MODE STARTED")

        while True:
            try:
                self.run_once()
                time.sleep(interval)

            except KeyboardInterrupt:
                print("\nStopped safely by user")
                break

            except Exception as e:
                print("Auto error:", e)
                print("Rolling back last session...")

                self.undo.undo_last_session()
