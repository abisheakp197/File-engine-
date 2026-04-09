import os
import shutil
from pathlib import Path

class FileRouter:
    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def move_files(self, files, target_folder):
        target_path = self.base_path / target_folder
        target_path.mkdir(exist_ok=True)

        moved_count = 0

        for f in files:
            try:
                source = Path(f["path"])
                destination = target_path / source.name

                shutil.move(str(source), str(destination))
                moved_count += 1

            except Exception as e:
                print(f"Error moving {f['name']}: {e}")

        return moved_count
