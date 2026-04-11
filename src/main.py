print("File Engine Started")

from scanner import FileScanner
from filter import FileFilter
from router import FileRouter

def run():
    path = "/storage/emulated/0"

    # Scan files
    scanner = FileScanner(path)
    files = scanner.scan()

    print(f"Total files: {len(files)}")

    # Apply filters
    file_filter = FileFilter(files)

    images = file_filter.images()
    large_files = file_filter.by_size(min_size=10 * 1024 * 1024)  # 10MB

    print(f"Images found: {len(images)}")
    print(f"Large files: {len(large_files)}")

    # 🔍 Debug preview
    print("\nSample images:")
    for img in images[:5]:
        print(img["path"])

    # 🚀 Routing (SAFE TEST MODE)
    router = FileRouter()

    print("\nMoving sample files...")

    router.move_files(images[:10], "Images")        # only 10 images
    router.move_files(large_files[:5], "LargeFiles")  # only 5 large files

if __name__ == "__main__":
    run()
