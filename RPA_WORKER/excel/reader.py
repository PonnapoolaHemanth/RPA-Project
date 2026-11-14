#Reading the Excel file and return the data.

import pandas as pd


def read_employee_file(file_path):
    try:
        data = pd.read_excel(file_path)

        return data

    except Exception as error:
        print(f"Error reading Excel file: {error}")
        raise
    