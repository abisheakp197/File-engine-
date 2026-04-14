import os
import time
import threading
import sys

# -------- Scanner (Generator) --------
def scan_files(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            yield os.path.join(root, file)

# -------- Preview Operation --------
def preview_rename(file_path, prefix):
    directory, filename = os.path.split(file_path)
    new_name = prefix + filename
    new_path = os.path.join(directory, new_name)

    return {
        "original": file_path,
        "preview": new_path
    }

# -------- Preview Engine --------
def generate_preview(folder_path, prefix):
    for file_path in scan_files(folder_path):
        yield preview_rename(file_path, prefix)

# -------- Stop Control --------
stop_requested = False

def listen_for_stop():
    global stop_requested
    while True:
        user_input = sys.stdin.read(1)
        if user_input.lower() == 'q':
            stop_requested = True
            print("\nStop requested by user...")
            break

# -------- Main Execution --------
if __name__ == "__main__":
    folder = "test_folder"
    prefix = "NEW_"

    start_time = time.time()

    # Start input listener thread
    input_thread = threading.Thread(target=listen_for_stop, daemon=True)
    input_thread.start()

    print("Press 'q' to stop...\n")
    print("=== Preview Sample ===")

    for i, item in enumerate(generate_preview(folder, prefix), start=1):

        # Stop if requested
        if stop_requested:
            print(f"\nStopped at {i} files.")
            break

        # Show first 20 preview results
        if i <= 20:
            print(item)

        elif i == 21:
            print("\n=== Processing Progress ===")

        # Show progress every 100 files
        if i % 100 == 0:
            elapsed = time.time() - start_time
            speed = i / elapsed if elapsed > 0 else 0

            print(f"Processed {i} files | Speed: {speed:.2f} files/sec")
