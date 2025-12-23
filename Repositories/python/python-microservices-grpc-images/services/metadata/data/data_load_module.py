import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_store = {}
metadata_index = {}


def load_data():
    data_file = "metadata.json"
    json_file = os.path.join(current_dir, data_file)
    with open(json_file, "r") as file:
        data_store[data_file] = json.load(file)


def build_metadata_index():
    global metadata_index
    metadata_data = data_store.get("metadata.json", [])
    for item in metadata_data:
        metadata_index[item["id"]] = item
