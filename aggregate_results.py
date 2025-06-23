import os
import json
import pandas as pd


# Path to folder containing results
RESULTS_FOLDER = "src/results/"
OUTPUT_FILE_CSV = "src/results/aggregated_results.csv"
OUTPUT_FILE_JSON = "src/results/aggregated_results.jsonl"

# Initialize list of results
records = []


def _is_result_file_json(filename: str) -> bool:
    """ 
    Check if results file ends with .json.
    
    Args:
        filename (str): name of the file.
        
    Returns:
        bool: True if the file ends with '.json', False otherwise.
    """
    
    return filename.endswith(".json")


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
                    records.append(data)
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON in: {filename}")
                    continue


# Step 2: Save to CSV
df = pd.DataFrame(records)
df.to_csv(OUTPUT_FILE_CSV, index=False)

print(f"✅ Aggregated {len(records)} entries into {RESULTS_FOLDER}")