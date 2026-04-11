import os

class FileScanner:
    def __init__(self, path):
        self.path = path

    def scan(self):
        all_files = []

        for root, dirs, files in os.walk(self.path):
            for file in files:
                full_path = os.path.join(root, file)

                try:
                    size = os.path.getsize(full_path)
                except:
                    size = 0

                extension = os.path.splitext(file)[1].lower()

                file_data = {
                    "path": full_path,
                    "name": file,
                    "extension": extension,
                    "size": size
                }

                all_files.append(file_data)

        return all_files
