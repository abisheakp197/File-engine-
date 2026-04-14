print("File Engine Started (SESSION MODE)")

import time
import threading

from scanner import FileScanner
from filter import FileFilter
from router import FileRouter
from logger import create_session

from control import reset_stop, should_stop, start_keyboard_listener


def print_group(title, items):
    print(f"\n=== {title} ({len(items)}) ===")
    for item in items[:10]:  # show only first 10 for clean UI
        print(f"[{item['ext']}] {item['name']} ({item['size']} bytes)")
    if len(items) > 10:
        print(f"... +{len(items) - 10} more")


def run():
    path = "/storage/emulated/0"

    # -------------------------
    # SESSION
    # -------------------------
    session_id = create_session()
    print("Session ID:", session_id)

    # -------------------------
    # SCAN (STREAM)
    # -------------------------
    scanner = FileScanner(path)
    file_stream = scanner.scan()

    # -------------------------
    # FILTER
    # -------------------------
    file_filter = FileFilter(file_stream)

    images_stream = file_filter.images()
    videos_stream = file_filter.videos()
    large_stream = file_filter.large_files(min_size_mb=10)

    images = list(images_stream)[:5]
    videos = list(videos_stream)[:5]
    large_files = list(large_stream)[:3]

    print(f"\nImages found: {len(images)}")
    print(f"Videos found: {len(videos)}")
    print(f"Large files found: {len(large_files)}")

    # -------------------------
    # PREVIEW MODE (SMART UI)
    # -------------------------
    choice = input("\nRun preview before moving? (y/n): ")

    if choice.lower() == "y":

        reset_stop()
        start_keyboard_listener()

        print("\nPress 'q' + Enter to stop preview...\n")

        start_time = time.time()

        # SMART GROUPED PREVIEW UI
        print_group("IMAGES", images)
        print_group("VIDEOS", videos)
        print_group("LARGE FILES", large_files)

        # simple progress simulation
        preview_data = images + videos + large_files

        for i, item in enumerate(preview_data):

            if should_stop():
                print("\n[STOPPED] by user")
                return

            if i % 100 == 0 and i > 0:
                elapsed = time.time() - start_time
                speed = i / elapsed if elapsed > 0 else 0
                print(f"\nProcessed {i} files | Speed: {speed:.2f} files/sec")

    # -------------------------
    # ROUTER
    # -------------------------
    router = FileRouter()

    print("\nMoving files...")

    if images:
        router.move_files(images, "Images", session_id)

    if videos:
        router.move_files(videos, "Videos", session_id)

    if large_files:
        router.move_files(large_files, "LargeFiles", session_id)

    print("\nSession completed successfully.")


if __name__ == "__main__":
    run()
