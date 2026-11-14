#It's determines whether the each employee is valid or invalid.
#Rules for now.
#Employee_ID → required
#Name        → required
#Email       → required
#Email       → valid format
#Department  → required
#Department  → IT / HR / Finance

import pandas as pd

REQUIRED_COLUMNS = {
    "Employee_ID",
    "Name",
    "Email",
    "Department"
}

ALLOWED_DEPARTMENTS = {
    "IT",
    "HR",
    "Finance"
}
#Without regular expressions we can validate email in this way.
def validate_email(email):
    #Checking empty and missing values.
    if pd.isna(email):
        return False
    
    #Converting the text to clean up space
    email = str(email).strip()

    #Checking for only one "@" symbol
    if email.count("@") != 1:
        return False
    
    #Spliting Email into two parts
    parts = email.split("@")
    username = parts[0]
    domain = parts[1]

    #Checking email field is not empyt.
    if not username:
        return False

    #Mail contains "." before domain
    if "." not in domain: 
        return False
    if domain.startswith(".") or domain.endswith("."):
         return False
    
    #ALl validations are correct then true.
    return True

#Validating name
def validate_name(name):
    if pd.isna(name):
        return False
    
    name = str(name).strip()

    if len(name) > 0:
        return True
    else:
        return False

#Validating Employee_id
def validate_employee_id(employee_id):
    if pd.isna(employee_id):
        return False

    if str(employee_id).strip() != "":
        return True
    else:
        return False

#Validating department
def validate_department(department):
    if pd.isna(department):
        return False
    department = str(department).strip()

    return department in ALLOWED_DEPARTMENTS

#Validating one employee at one time.
def validate_employee(row, duplicate_ids):
    errors = []

    employee_id = row["Employee_ID"]

    if not validate_employee_id(row["Employee_ID"]):
        errors.append("Employee ID is required")
    #Checking for the duplicate ids.
    elif employee_id in duplicate_ids:
        errors.append("Duplicate Employee ID")

    if not validate_name(row["Name"]):
        errors.append("Name is required")

    if pd.isna(row["Email"]) or not validate_email(row["Email"]):
        errors.append("Invalid or missing email")

    if not validate_department(row["Department"]):
        errors.append("Invalid or missing department")

    if errors:
        return {
            "Status": "INVALID",
            "Message": "; ".join(errors)
        }

    return {
        "Status": "VALID",
        "Message": "Validation successful"
    }

#Validating entire DtatFrame.
def validate_employees(data):
    #Checking whether data was successfully loaded.
    if data is None:
        raise ValueError(
            "Employee data is empty or could not be read."
        )

    #Checking whether excel file contains any records
    if data.empty:
        raise ValueError(
            "Employee Excel file contains no employee records."
        )
    provided_columns = set(data.columns)

    missing_columns = []
    for col in REQUIRED_COLUMNS:
        if col not in provided_columns:
            missing_columns.append(col)

    if len(missing_columns) > 0:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")

    is_duplicate_mask = data["Employee_ID"].duplicated(keep=False)
    duplicate_rows = data.loc[is_duplicate_mask]
    duplicate_ids = set(duplicate_rows["Employee_ID"])

    results = []

    for row in data.to_dict(orient="records"):
        employee_result = validate_employee(row, duplicate_ids)
        results.append(employee_result)

    return results
