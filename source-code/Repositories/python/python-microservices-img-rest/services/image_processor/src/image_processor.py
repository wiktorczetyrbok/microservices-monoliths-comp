
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageOps
import os
import uuid

app = Flask(__name__)
OUTPUT_FOLDER = "/tmp/image_results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/process", methods=["POST"])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    operation = request.form.get("operation", "grayscale")
    image_file = request.files["image"]
    task_id = str(uuid.uuid4())
    input_path = os.path.join(OUTPUT_FOLDER, f"{task_id}_input.png")
    output_path = os.path.join(OUTPUT_FOLDER, f"{task_id}_output.png")
    image_file.save(input_path)

    try:
        image = Image.open(input_path)
        if operation == "grayscale":
            processed = ImageOps.grayscale(image)
        elif operation == "invert":
            processed = ImageOps.invert(image.convert("RGB"))
        else:
            return jsonify({"error": "Unsupported operation"}), 400

        processed.save(output_path)
        return jsonify({"task_id": task_id, "result": f"/result/{task_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    output_path = os.path.join(OUTPUT_FOLDER, f"{task_id}_output.png")
    if not os.path.exists(output_path):
        return jsonify({"error": "Result not found"}), 404
    return send_file(output_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
