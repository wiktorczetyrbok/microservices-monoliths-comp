
from flask import Flask, request, jsonify
import os
import uuid
import json

app = Flask(__name__)
TASK_FOLDER = "/tmp/tasks"
os.makedirs(TASK_FOLDER, exist_ok=True)

@app.route("/task", methods=["POST"])
def submit_task():
    data = request.form.to_dict()
    if "operation" not in data:
        return jsonify({"error": "Missing operation"}), 400

    task_id = str(uuid.uuid4())
    task_data = {
        "id": task_id,
        "status": "pending",
        "operation": data["operation"]
    }

    task_path = os.path.join(TASK_FOLDER, f"{task_id}.json")
    with open(task_path, "w") as f:
        json.dump(task_data, f)

    return jsonify({"task_id": task_id, "status": "pending"}), 200

@app.route("/task/<task_id>", methods=["GET"])
def get_task_status(task_id):
    task_path = os.path.join(TASK_FOLDER, f"{task_id}.json")
    if not os.path.exists(task_path):
        return jsonify({"error": "Task not found"}), 404

    with open(task_path, "r") as f:
        task_data = json.load(f)

    return jsonify(task_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
