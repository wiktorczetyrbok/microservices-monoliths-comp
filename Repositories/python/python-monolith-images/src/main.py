import logging
from flask import Flask, request, jsonify

from src.data_load_module import image_buffers
from src.features import extract_features
from src.similarity import find_similar_images
from src.metadata import get_image_metadata

app = Flask(__name__)


@app.route("/images/search", methods=["GET"])
def search_images():
    try:
        kernel = int(request.args.get("kernel"))
        threshold = float(request.args.get("threshold"))

        # Fixed reference image (like geo center)
        image_id = "img001"

        query_image = image_buffers[image_id]

        query_vector = extract_features(query_image, kernel)
        matches = find_similar_images(query_vector, threshold)

        if not matches:
            return jsonify([])

        return jsonify(get_image_metadata(matches))

    except Exception as e:
        logging.exception(e)
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
