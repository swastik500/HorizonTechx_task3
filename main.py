from pathlib import Path
from datetime import datetime
import shutil
import time
import sys

# ---------------- CONFIGURATION ----------------
BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "source"
DESTINATION_DIR = BASE_DIR / "organized"
REPORT_DIR = BASE_DIR / "reports"

IMAGE_EXTENSIONS = {".jpg", ".jpeg"}

# ---------------- TERMINAL COLORS ----------------
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def color(text, shade):
    return f"{shade}{text}{Colors.RESET}"

def banner():
    print(color(r"""
╔════════════════════════════════════════════════════╗
║              SMART JPG ORGANIZER                ║
║        Python File Automation Project           ║
╚════════════════════════════════════════════════════╝
""", Colors.CYAN))

def get_jpg_files():
    """Return JPG/JPEG files directly inside the source folder."""
    return sorted(
        file for file in SOURCE_DIR.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

def unique_destination(path):
    """Avoid overwriting an existing file by adding a numbered suffix."""
    if not path.exists():
        return path

    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1

def show_progress(current, total, width=30):
    ratio = current / total if total else 1
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(ratio * 100)
    print(f"\r  [{bar}] {percent:3d}% ({current}/{total})", end="", flush=True)

def write_report(moved_files, preview=False):
    REPORT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = REPORT_DIR / f"organizer_report_{timestamp}.txt"

    with report_path.open("w", encoding="utf-8") as report:
        report.write("SMART JPG ORGANIZER REPORT\n")
        report.write("=" * 35 + "\n")
        report.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Mode: {'PREVIEW' if preview else 'ORGANIZE'}\n")
        report.write(f"Source: {SOURCE_DIR}\n")
        report.write(f"Destination: {DESTINATION_DIR}\n")
        report.write(f"Images {'found' if preview else 'moved'}: {len(moved_files)}\n\n")
        report.write("Files:\n")
        for file_name in moved_files:
            report.write(f"- {file_name}\n")

    return report_path

def main():
    banner()

    # Ensure expected folders exist
    SOURCE_DIR.mkdir(exist_ok=True)
    DESTINATION_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    print(color("Choose a mode:", Colors.BOLD))
    print("  1. Organize files (move JPG/JPEG images)")
    print("  2. Preview (show what would be moved)")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice not in {"1", "2"}:
        print(color("\nInvalid choice. Run the script again and enter 1 or 2.", Colors.RED))
        return

    preview = choice == "2"
    files = get_jpg_files()

    print(f"\nSource folder:      {SOURCE_DIR}")
    print(f"Destination folder: {DESTINATION_DIR}")
    print(f"JPG/JPEG found:    {len(files)}")

    if not files:
        print(color("\nNo JPG/JPEG files found in the source folder.", Colors.YELLOW))
        print("Add a few images to 'source' and run again.")
        return

    if preview:
        print(color("\nPREVIEW MODE: no files will be moved.\n", Colors.YELLOW))
    else:
        confirmation = input("\nMove these files? (y/n): ").strip().lower()
        if confirmation != "y":
            print(color("Cancelled. No files were moved.", Colors.YELLOW))
            return

    moved_or_previewed = []
    errors = []

    print("\nProcessing files...")
    for index, file_path in enumerate(files, start=1):
        destination_path = unique_destination(DESTINATION_DIR / file_path.name)

        try:
            if not preview:
                shutil.move(str(file_path), str(destination_path))
            moved_or_previewed.append(destination_path.name)
        except OSError as error:
            errors.append(f"{file_path.name}: {error}")

        show_progress(index, len(files))
        time.sleep(0.08)  # Small delay so the progress bar is visible

    print("\n")

    if preview:
        print(color("Preview complete! Files remain in the source folder.", Colors.YELLOW))
    else:
        print(color("Organization complete!", Colors.GREEN))

    print(f"Images {'previewed' if preview else 'moved'}: {len(moved_or_previewed)}")

    if errors:
        print(color(f"Errors: {len(errors)}", Colors.RED))
        for error in errors:
            print(f"  - {error}")

    report_path = write_report(moved_or_previewed, preview)
    print(f"Report saved: {report_path}")

    if not preview and not errors:
        print(color("\n✨ Your folders are looking fresh. Mission accomplished! ✨", Colors.MAGENTA))

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\nStopped by user.", Colors.YELLOW))
        sys.exit(0)
