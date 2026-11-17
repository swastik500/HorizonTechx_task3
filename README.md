# Smart JPG Organizer

A beginner-friendly Python automation project that moves JPG/JPEG images from a source folder into an organized destination folder.

## Features
- Moves `.jpg` and `.jpeg` files
- Preview mode
- Progress bar
- Duplicate filename protection
- Text report with date/time
- Colorful terminal output

## Requirements
- Python 3.9 or newer
- No third-party packages required

## Run
1. Put JPG/JPEG images in the `source` folder.
2. Open a terminal in this project folder.
3. Run:

   ```bash
   python main.py
   ```

4. Choose `1` to organize or `2` to preview.

## Folders
- `source/`: images waiting to be organized
- `organized/`: moved images
- `reports/`: generated reports

The script processes files directly inside `source/`, not nested subfolders.
