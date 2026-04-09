import os
from pathlib import Path

class FileScanner:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.files = []

    def scan(self):
        """Scan all files including subfolders"""
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                file_info = self.get_file_info(file_path)
                self.files.append(file_info)
        return self.files

    def get_file_info(self, file_path):
        """Extract useful file metadata"""
        return {
            "name": file_path.name,
            "path": str(file_path),
            "size": file_path.stat().st_size,
            "extension": file_path.suffix.lower()
        }


if __name__ == "__main__":
    scanner = FileScanner("/storage/emulated/0")  # Android root
    results = scanner.scan()

    print(f"Total files found: {len(results)}")
    print(results[:5])  # preview first 5
