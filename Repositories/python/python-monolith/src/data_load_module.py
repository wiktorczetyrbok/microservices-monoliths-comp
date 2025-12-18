import json
import os
from collections import defaultdict


current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")
data_store = {}

hotel_geo_data = {}
inventory_index = defaultdict(lambda: defaultdict(dict))
hotel_profiles_index = {}


def load_data():
    file_names = ["geo.json", "hotels.json", "inventory.json"]
    for json_file in file_names:
        file_path = os.path.join(data_dir, json_file)
        try:
            with open(file_path, "r") as file:
                data_store[json_file] = json.load(file)
        except FileNotFoundError:
            print(f"Error: File {json_file} not found in {data_dir}")
        except json.JSONDecodeError:
            print(f"Error: File {json_file} is not a valid JSON file")


def build_hotel_geo_data():
    global hotel_geo_data
    hotels = data_store.get("geo.json", [])

    for item in hotels:
        hotel_id = item["hotelId"]
        hotel_geo_data[hotel_id] = {'lat': item['lat'], 'lon': item['lon'], 'data': item}


def build_inventory_index():
    global inventory_index
    inventory_data = data_store.get("inventory.json", [])

    for item in inventory_data:
        hotel_id = item["hotelId"]
        in_date = item["inDate"]
        out_date = item["outDate"]
        inventory_index[hotel_id][in_date][out_date] = item


def build_hotel_profiles_index():
    global hotel_profiles_index
    hotel_profiles_data = data_store.get("hotels.json", [])
    for hotel in hotel_profiles_data:
        hotel_id = hotel["id"]
        hotel_profiles_index[hotel_id] = hotel


load_data()
build_hotel_geo_data()
build_inventory_index()
build_hotel_profiles_index()