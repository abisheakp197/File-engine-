import os
import shutil
import json

class FileRouter:
    def __init__(self):
        self.base_path = "/storage/emulated/0/Organized"
        self.log_file = "/storage/emulated/0/undo_log.json"

    def move_files(self, files, folder_name):
        target_folder = os.path.join(self.base_path, folder_name)
        os.makedirs(target_folder, exist_ok=True)

        log_data = []

        # Load existing log if exists
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    log_data = json.load(f)
            except:
                log_data = []

        moved = 0

        for file in files:
            src = file["path"]
            filename = file["name"]
            dest = os.path.join(target_folder, filename)

            try:
                shutil.move(src, dest)

                # Save move info
                log_data.append({
                    "from": src,
                    "to": dest
                })

                moved += 1

            except Exception as e:
                pass

        # Save log
        with open(self.log_file, "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"Moved {moved} files to {folder_name}")
