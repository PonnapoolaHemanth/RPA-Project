#Extracting the validated results(employee data) and creates a new excel file as a Employee_result.xlsx
from pathlib import Path
import pandas as pd

def write_result_file(data, validation_results, output_path):
    if len(data) != len(validation_results):
        raise ValueError(
            "Number of employees and validation results do not match."
        )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
     
    result_data = data.copy()

    status_list = []
    message_list = []

    for result in validation_results:
        status_list.append(result["Status"])
        message_list.append(result["Message"])

    result_data["Status"] = status_list
    result_data["Message"] = message_list

    result_data.to_excel(output_path, index=False)

    return output_path