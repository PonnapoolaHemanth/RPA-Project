import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExcelFileHandler(FileSystemEventHandler):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Ignore temporary Excel files
        if file_path.name.startswith("~$"):
            return

        # Only process .xlsx files
        if file_path.suffix.lower() != ".xlsx":
            return

        print(f"New Excel file detected: {file_path}")

        # Wait until the file is completely copied
        if self.wait_for_file(file_path):

            print(f"File is ready: {file_path}")

            self.callback(file_path)

        else:

            print(f"File is not ready: {file_path}")

    def wait_for_file(
        self,
        file_path,
        wait_time=1,
        max_attempts=10
    ):
        """
        Wait until the file size remains unchanged.
        """

        previous_size = -1

        for attempt in range(max_attempts):

            if not file_path.exists():
                return False

            current_size = file_path.stat().st_size

            print(
                f"Checking file... "
                f"attempt {attempt + 1}: "
                f"{current_size} bytes"
            )

            if current_size == previous_size:
                return True

            previous_size = current_size

            time.sleep(wait_time)

        return False


def start_watcher(folder_path, callback):

    event_handler = ExcelFileHandler(callback)

    observer = Observer()

    observer.schedule(
        event_handler,
        folder_path,
        recursive=False
    )

    observer.start()

    print(f"Watching folder: {folder_path}")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping folder watcher...")

        observer.stop()

    observer.join()