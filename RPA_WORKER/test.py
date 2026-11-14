from pathlib import Path

from excel.reader import read_employee_file
from excel.validator import validate_employees
from excel.writer import write_result_file


BASE_DIR = Path(__file__).resolve().parent

input_file = BASE_DIR / "input" / "Employee.xlsx"
output_file = BASE_DIR / "output" / "Employee_result.xlsx"


print("Reading Excel file...")

employees = read_employee_file(input_file)

print(f"Employees found: {len(employees)}")

print("Validating employees...")

validation_results = validate_employees(employees)

print("Creating result file...")

result_file = write_result_file(
    employees,
    validation_results,
    output_file
)

print(f"Result file created: {result_file}")

#Secret key 
#import secrets
#print(secrets.token_hex(32))