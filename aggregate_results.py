import os
import json
import pandas as pd


# Path to folder containing results
RESULTS_FOLDER = "src/results/"
OUTPUT_FILE_CSV = "src/results/aggregated_results.csv"
OUTPUT_FILE_JSON = "src/results/aggregated_results.jsonl"
OUTPUT_FILE_XLSX = "src/results/aggregated_results.xlsx"
INVALID_FILE_XLSX = "src/results/invalid_results.xlsx"

REQUIRED_FIELDS = [
    "Formulation", "MILP Objective", "Upper Bound", "Relative Gap",
    "Time (s)", "MILP Status", "MILP Term. Condition", "LP Relaxation",
    "Num. Binary Var.", "Total Num. Var.", "Num. Constraints"
]

# Initialize list of results
valid_records = []
invalid_records = []


def _is_result_file_json(filename: str) -> bool:
    """ 
    Check if results file ends with .json.
    
    Args:
        filename (str): name of the file.
        
    Returns:
        bool: True if the file ends with '.json', False otherwise.
    """
    
    return filename.endswith(".json")


def _is_valid_record(record: dict) -> bool:
    """
    A record is valid if all required fields are not None.
    
    Args:
        record (dict): dictionary with results from a run.
        
    Returns:
        bool: True if the dictionary has no Null in the important fields.
    """

    return all(record.get(field) is not None for field in REQUIRED_FIELDS)


# Step 1: Loops through each file in the results folder and add the content of json files to records 
for filename in os.listdir(RESULTS_FOLDER):
    if not _is_result_file_json(filename):
        continue

    filepath = os.path.join(RESULTS_FOLDER, filename)

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            
            if line.startswith("{") and line.endswith("}"):
                try:
                    data = json.loads(line)
                    if _is_valid_record(data):
                        data["Instance"] = data["Instance"][:25]
                        valid_records.append(data)
                    else:
                        invalid_records.append(data)
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON in: {filename}")
                    continue

df_invalid = pd.DataFrame(invalid_records)
df_valid = pd.DataFrame(valid_records)

# Step 2: Save to CSV
#df_valid.to_csv(OUTPUT_FILE_CSV, index=False)

# Step 3: Save to Excel
df_valid.to_excel(OUTPUT_FILE_XLSX, index=False, sheet_name="Valid Records")
df_invalid.to_excel(INVALID_FILE_XLSX, index=False, sheet_name="Invalid Records")


print(f"✅ Aggregated {len(df_valid)} entries into {RESULTS_FOLDER}")
print(f"⚠️ Skipped {len(invalid_records)} invalid entries (see 'Invalid Records' tab in Excel).")