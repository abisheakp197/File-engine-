import os


class FileScanner:

    def __init__(self, root_path):
        self.root_path = root_path

        self.ignore_folders = {
            "/storage/emulated/0/Images",
            "/storage/emulated/0/LargeFiles",
            "/storage/emulated/0/storage",
            "/storage/emulated/0/File-engine-",
            "/storage/emulated/0/Android/data",
            "/storage/emulated/0/Android/obb"
        }

    # -------------------------
    # STREAMING SCANNER (CONTROLLED)
    # -------------------------
    def scan(self):
        from control import should_stop  # <-- SAFE ADDITION ONLY

        for root, dirs, files in os.walk(self.root_path):

            # STOP CHECK (outer loop)
            if should_stop():
                return

            if self._is_ignored(root):
                continue

            for file in files:

                # STOP CHECK (inner loop)
                if should_stop():
                    return

                full_path = os.path.join(root, file)

                try:
                    size = os.path.getsize(full_path)

                    _, ext = os.path.splitext(file)
                    ext = ext.lower()

                    yield {
                        "path": full_path,
                        "name": file,
                        "size": size,
                        "ext": ext
                    }

                except:
                    continue

    # -------------------------
    # IGNORE LOGIC (UNCHANGED)
    # -------------------------
    def _is_ignored(self, path):
        for ignore in self.ignore_folders:
            if path.startswith(ignore):
                return True
        return False
