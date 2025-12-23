import json
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, "images")

image_buffers = {}


def load_data():
    build_image_buffers()


def build_image_buffers():
    global image_buffers
    for file in os.listdir(image_dir):
        path = os.path.join(image_dir, file)
        if os.path.isfile(path):
            image_id = os.path.splitext(file)[0]
            with open(path, "rb") as f:
                image_buffers[image_id] = f.read()
