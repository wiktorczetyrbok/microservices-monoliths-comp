
from flask import Flask, request, jsonify, send_from_directory
import os
import uuid

app = Flask(__name__)
STORAGE_FOLDER = "/tmp/storage"
os.makedirs(STORAGE_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_id = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(STORAGE_FOLDER, file_id)
    file.save(file_path)

    return jsonify({"filename": file_id, "path": f"/download/{file_id}"}), 200

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(STORAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(STORAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
