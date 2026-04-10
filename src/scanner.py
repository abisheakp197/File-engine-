import os
from pathlib import Path

# =========================
# CONFIG
# =========================

ANDROID_ROOT = "/storage/emulated/0"

SCAN_PATHS = [
    f"{ANDROID_ROOT}/Download",
    f"{ANDROID_ROOT}/DCIM",
    f"{ANDROID_ROOT}/Documents"
]

# =========================
# SCANNER
# =========================

class FileScanner:
    def __init__(self, paths):
        self.paths = [Path(p) for p in paths]
        self.files = []

    def scan(self):
        """Scan all configured paths safely"""
        for root_path in self.paths:
            print(f"[SCAN] {root_path}")
            for file_path in self.safe_rglob(root_path):
                if file_path.is_file():
                    file_info = self.get_file_info(file_path)
                    if file_info:
                        self.files.append(file_info)
        return self.files

    def safe_rglob(self, root):
        """Safe recursive scan"""
        try:
            for item in root.iterdir():
                yield item
                if item.is_dir():
                    yield from self.safe_rglob(item)
        except PermissionError:
            print(f"[SKIPPED] No permission: {root}")
        except Exception as e:
            print(f"[ERROR] {root}: {e}")

    def get_file_info(self, file_path):
        """Get metadata safely"""
        try:
            return {
                "name": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "extension": file_path.suffix.lower()
            }
        except Exception as e:
            print(f"[FAILED] {file_path}: {e}")
            return None


# =========================
# TEST RUN
# =========================

if __name__ == "__main__":
    scanner = FileScanner(SCAN_PATHS)
    results = scanner.scan()

    print(f"\nTotal files found: {len(results)}")
    print(results[:5])
