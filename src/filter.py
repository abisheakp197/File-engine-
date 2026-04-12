class FileFilter:

    def __init__(self, files):
        self.files = files

        # -------------------------
        # SAFETY: NEVER TOUCH THESE
        # -------------------------
        self.ignore_paths = [
            "/storage/emulated/0/File-engine-",
            "/storage/emulated/0/storage/history",
            "/storage/emulated/0/Images",
            "/storage/emulated/0/LargeFiles",
            "/storage/emulated/0/Android/data",
            "/storage/emulated/0/Android/obb"
        ]

        # -------------------------
        # SAFE FILE TYPES ONLY
        # -------------------------
        self.blocked_extensions = [
            ".py",
            ".json",
            ".log",
            ".db",
            ".xml"
        ]

    # -------------------------
    # CORE SAFETY CHECK
    # -------------------------
    def _is_safe(self, file):
        path = file["path"]

        # block system paths
        for ignore in self.ignore_paths:
            if path.startswith(ignore):
                return False

        # block sensitive file types
        ext = file.get("extension", "").lower()
        if ext in self.blocked_extensions:
            return False

        return True

    # -------------------------
    # FILTER: IMAGES
    # -------------------------
    def images(self):
        safe_files = [f for f in self.files if self._is_safe(f)]
        return self.by_extension(safe_files, [".jpg", ".jpeg", ".png"])

    # -------------------------
    # FILTER: LARGE FILES
    # -------------------------
    def by_size(self, min_size=10):
        safe_files = [f for f in self.files if self._is_safe(f)]
        return [f for f in safe_files if f["size"] >= min_size * 1024 * 1024]

    # -------------------------
    # INTERNAL: EXTENSION FILTER
    # -------------------------
    def by_extension(self, file_list, extensions):
        return [
            f for f in file_list
            if f.get("extension", "").lower() in extensions
        ]
