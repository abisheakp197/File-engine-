print("File Engine Started")

from scanner import FileScanner
from filter import FileFilter

def run():
    path = "/storage/emulated/0"

    scanner = FileScanner(path)
    files = scanner.scan()

    print(f"Total files: {len(files)}")

    # Apply filters
    file_filter = FileFilter(files)

    images = file_filter.images()
    large_files = file_filter.by_size(min_size=100000000)  # 100MB+

    print(f"Images found: {len(images)}")
    print(f"Large files: {len(large_files)}")

if __name__ == "__main__":
    run()
