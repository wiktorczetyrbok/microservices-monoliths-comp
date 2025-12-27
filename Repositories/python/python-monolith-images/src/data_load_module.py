import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")
image_dir = os.path.join(data_dir, "images")

image_buffers = {}
feature_index = {}
metadata_index = {}


def load_json(filename):
    with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
        return json.load(f)




def load_images():
    for file in os.listdir(image_dir):
        image_id = os.path.splitext(file)[0]
        with open(os.path.join(image_dir, file), "rb") as f:
            image_buffers[image_id] = f.read()


def load_data():
    load_images()

    for item in load_json("features.json"):
        feature_index[item["id"]] = item["vector"]

    for item in load_json("metadata.json"):
        metadata_index[item["id"]] = item

    print(
        f"[DATA] Loaded {len(image_buffers)} images, "
        f"{len(feature_index)} feature vectors, "
        f"{len(metadata_index)} metadata records"
    )


load_data()
