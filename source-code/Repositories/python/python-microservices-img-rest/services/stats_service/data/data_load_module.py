import json
import os
from collections import defaultdict

current_dir = os.path.dirname(os.path.abspath(__file__))
data_store = {}

inventory_index = defaultdict(lambda: defaultdict(dict))


def load_data():
    data_file = "inventory.json"
    json_file = os.path.join(current_dir, data_file)
    try:
        with open(json_file, "r") as file:
            data_store[data_file] = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {data_file} not found in {json_file}")
    except json.JSONDecodeError:
        print(f"Error: File {data_file} is not a valid JSON file")


def build_inventory_index():
    global inventory_index
    inventory_data = data_store.get("inventory.json", [])

    for item in inventory_data:
        hotel_id = item["hotelId"]
        in_date = item["inDate"]
        out_date = item["outDate"]
        inventory_index[hotel_id][in_date][out_date] = item


load_data()
build_inventory_index()
