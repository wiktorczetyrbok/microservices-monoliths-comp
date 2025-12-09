import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_store = {}
hotel_geo_data = {}


def load_data():
    data_file = "geo.json"
    json_file = os.path.join(current_dir, data_file)
    try:
        with open(json_file, "r") as file:
            data_store[data_file] = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {data_file} not found in {json_file}")
    except json.JSONDecodeError:
        print(f"Error: File {data_file} is not a valid JSON file")


def build_hotel_geo_data():
    global hotel_geo_data
    hotels = data_store.get("geo.json", [])

    for item in hotels:
        hotel_id = item["hotelId"]
        hotel_geo_data[hotel_id] = {
            "lat": item["lat"],
            "lon": item["lon"],
            "data": item,
        }


load_data()
build_hotel_geo_data()
