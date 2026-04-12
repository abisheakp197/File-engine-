print("File Engine Started (SESSION MODE)")

from scanner import FileScanner
from filter import FileFilter
from router import FileRouter
from logger import create_session


def run():
    path = "/storage/emulated/0"

    # -------------------------
    # CREATE SESSION
    # -------------------------
    session_id = create_session()
    print("Session ID:", session_id)

    # -------------------------
    # SCAN
    # -------------------------
    scanner = FileScanner(path)
    files = scanner.scan()

    print(f"Total files: {len(files)}")

    # -------------------------
    # FILTER
    # -------------------------
    file_filter = FileFilter(files)

    images = file_filter.images()
    large_files = file_filter.by_size(min_size=10)

    print(f"Images found: {len(images)}")
    print(f"Large files: {len(large_files)}")

    # -------------------------
    # ROUTE (SESSION TRACKED)
    # -------------------------
    router = FileRouter()

    print("\nMoving files...")

    router.move_files(images[:5], "Images", session_id)
    router.move_files(large_files[:3], "LargeFiles", session_id)

    print("\nSession completed successfully.")


if __name__ == "__main__":
    run()
