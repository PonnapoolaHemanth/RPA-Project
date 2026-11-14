from pathlib import Path

from watcher.folder_watcher import start_watcher


BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"

start_watcher(INPUT_DIR)