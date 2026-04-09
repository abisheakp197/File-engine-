print("File Engine Started")

from scanner import FileScanner

def run():
    path = "/storage/emulated/0"  # Android storage

    scanner = FileScanner(path)
    files = scanner.scan()

    print(f"Total files scanned: {len(files)}")

    # Preview first few files
    for f in files[:5]:
        print(f)

if __name__ == "__main__":
    run()
