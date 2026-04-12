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

    def scan(self):
        all_files = []

        for root, dirs, files in os.walk(self.root_path):

            if self._is_ignored(root):
                continue

            for file in files:
                full_path = os.path.join(root, file)

                try:
                    size = os.path.getsize(full_path)

                    # ⭐ FIX: extract extension safely
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()

                    all_files.append({
                        "path": full_path,
                        "name": file,
                        "size": size,
                        "extension": ext
                    })

                except:
                    continue

        return all_files

    def _is_ignored(self, path):
        for ignore in self.ignore_folders:
            if path.startswith(ignore):
                return True
        return False
