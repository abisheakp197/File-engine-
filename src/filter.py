class FileFilter:
    def __init__(self, files):
        self.files = files

    def by_extension(self, extensions):
        """Filter files by extension"""
        return [f for f in self.files if f["extension"] in extensions]

    def by_size(self, min_size=0, max_size=None):
        """Filter files by size (bytes)"""
        result = []

        for f in self.files:
            if f["size"] >= min_size:
                if max_size is None or f["size"] <= max_size:
                    result.append(f)

        return result

    def images(self):
        return self.by_extension([".jpg", ".png", ".jpeg"])

    def videos(self):
        return self.by_extension([".mp4", ".mkv", ".avi"])
