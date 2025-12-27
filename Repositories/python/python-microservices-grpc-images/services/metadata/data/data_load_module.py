import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
metadata_index = {}


def load_data():
    path = os.path.join(current_dir, "metadata.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        metadata_index[item["id"]] = item

    print(f"[METADATA] Loaded {len(metadata_index)} records")