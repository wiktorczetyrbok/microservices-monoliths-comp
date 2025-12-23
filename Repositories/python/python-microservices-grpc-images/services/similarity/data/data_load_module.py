import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_store = {}
feature_index = {}


def load_data():
    data_file = "features.json"
    json_file = os.path.join(current_dir, data_file)
    with open(json_file, "r") as file:
        data_store[data_file] = json.load(file)


def build_feature_index():
    global feature_index
    features = data_store.get("features.json", [])
    for item in features:
        feature_index[item["id"]] = item["vector"]