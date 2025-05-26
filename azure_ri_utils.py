import json
import os

def get_mock_ri_usage(file_path="data/mock_ri_usage.json"):
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File '{file_path}' is empty.")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
