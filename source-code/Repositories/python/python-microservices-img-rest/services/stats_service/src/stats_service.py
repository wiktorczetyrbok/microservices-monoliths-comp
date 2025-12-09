
from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
STATS_FILE = "/tmp/stats.json"

# Ensure stats file exists
if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w") as f:
        json.dump({}, f)

@app.route("/log", methods=["POST"])
def log_stat():
    data = request.get_json()
    if "operation" not in data:
        return jsonify({"error": "Missing 'operation' in request"}), 400

    with open(STATS_FILE, "r") as f:
        stats = json.load(f)

    op = data["operation"]
    stats[op] = stats.get(op, 0) + 1

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

    return jsonify({"message": "Stat logged"}), 200

@app.route("/stats", methods=["GET"])
def get_stats():
    with open(STATS_FILE, "r") as f:
        stats = json.load(f)
    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
