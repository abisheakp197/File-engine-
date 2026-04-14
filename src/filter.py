class FileFilter:

    def __init__(self, files):
        self.files = files

        # -------------------------
        # SAFETY PATHS
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
        # EXTENSIONS
        # -------------------------
        self.image_ext = [".jpg", ".jpeg", ".png", ".webp"]

        self.video_ext = [
            ".mp4", ".mkv", ".mov", ".avi", ".3gp", ".webm"
        ]

        self.blocked_extensions = [
            ".py", ".json", ".log", ".db", ".xml"
        ]

    # -------------------------
    # CORE SAFETY CHECK
    # -------------------------
    def _is_safe(self, file):
        path = file["path"]

        for ignore in self.ignore_paths:
            if path.startswith(ignore):
                return False

        ext = file.get("ext", "").lower()

        if ext in self.blocked_extensions:
            return False

        return True

    # -------------------------
    # IMAGES STREAM
    # -------------------------
    def images(self):
        return (
            f for f in self.files
            if self._is_safe(f) and f.get("ext", "").lower() in self.image_ext
        )

    # -------------------------
    # VIDEOS STREAM
    # -------------------------
    def videos(self):
        return (
            f for f in self.files
            if self._is_safe(f) and f.get("ext", "").lower() in self.video_ext
        )

    # -------------------------
    # LARGE FILES STREAM (MB BASED)
    # -------------------------
    def large_files(self, min_size_mb=10):
        min_size = min_size_mb * 1024 * 1024

        return (
            f for f in self.files
            if self._is_safe(f) and f["size"] >= min_size
        )
