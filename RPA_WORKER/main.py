#It's a coordinator. Everything connects here.

#Step-1: Watcher
#Step-2: Reader
#Step-3: Validator
#Step-4: Writer


#Work-Flow:
#Start
# ↓
#Watch input/
# ↓
#Employee.xlsx detected
# ↓
#Read Excel
# ↓
#Validate
# ↓
#Write result
# ↓
#Move original file
# ↓
#Wait for next file

from pathlib import Path

from excel.reader import read_employee_file
from excel.validator import validate_employees
from excel.writer import write_result_file
from watcher.folder_watcher import start_watcher


BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
PROCESSED_DIR = BASE_DIR / "processed"
FAILED_DIR = BASE_DIR / "failed"

def process_file(file_path):

    print()
    print("=" * 50)
    print(f"Processing file: {file_path.name}")
    print("=" * 50)

    try:

        # 1. Read Excel
        print("Step 1: Reading Excel...")

        employees = read_employee_file(file_path)

        print(
            f"Employees found: {len(employees)}"
        )

        # 2. Validate employees
        print("Step 2: Validating employees...")

        validation_results = validate_employees(
            employees
        )

        # 3. Create output file
        print("Step 3: Creating result file...")

        output_file = (
            OUTPUT_DIR
            / f"{file_path.stem}_result.xlsx"
        )

        result_file = write_result_file(
            employees,
            validation_results,
            output_file
        )

        print(
            f"Result file created: {result_file}"
        )
        
        # 4. Move original file to processed/
        processed_file = (
            PROCESSED_DIR
            / file_path.name
        )

        file_path.rename(processed_file)

        print(
            f"Original file moved to: "
            f"{processed_file}"
        )

        print("=" * 50)
        print("Processing completed successfully.")
        print("=" * 50)

    except Exception as error:

        print()
        print("=" * 50)
        print("PROCESSING FAILED")
        print("=" * 50)

        print(f"Error: {error}")

        # Move failed file to failed/
        if file_path.exists():

            failed_file = (
                FAILED_DIR
                / file_path.name
            )

            file_path.rename(failed_file)

            print(
                f"Failed file moved to: "
                f"{failed_file}"
            )

        print("=" * 50)

def main():

    print("=" * 50)
    print("CUSTOM RPA WORKER STARTED")
    print("=" * 50)

    INPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FAILED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"Input folder : {INPUT_DIR}")
    print(f"Output folder: {OUTPUT_DIR}")
    print()

    start_watcher(
        INPUT_DIR,
        process_file
    )


if __name__ == "__main__":
    main()