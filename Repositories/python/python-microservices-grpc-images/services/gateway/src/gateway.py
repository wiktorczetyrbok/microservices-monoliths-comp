import logging
import grpc
from flask import Flask, request, jsonify

from proto import search_pb2, search_pb2_grpc
from proto import metadata_pb2, metadata_pb2_grpc

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

PORT = 8080
SEARCH_SERVICE = "search:8080"
METADATA_SERVICE = "metadata:8080"


@app.route("/images/search", methods=["GET"])
def search_images():
    kernel = int(request.args.get("kernel"))
    threshold = float(request.args.get("threshold"))

    logging.info(f"[GATEWAY] kernel={kernel} threshold={threshold}")

    # ---- SEARCH ----
    try:
        with grpc.insecure_channel(SEARCH_SERVICE) as channel:
            search_stub = search_pb2_grpc.SearchStub(channel)
            search_res = search_stub.Search(
                search_pb2.SearchRequest(
                    kernel=kernel,
                    threshold=threshold,
                )
            )
    except grpc.RpcError as e:
        logging.error(f"[SEARCH] unavailable: {e}")
        return jsonify({"error": "Search unavailable"}), 503

    if not search_res.imageIds:
        return jsonify([])

    # ---- METADATA ----
    try:
        with grpc.insecure_channel(METADATA_SERVICE) as channel:
            metadata_stub = metadata_pb2_grpc.MetadataStub(channel)
            meta_res = metadata_stub.Get(
                metadata_pb2.MetadataRequest(
                    imageIds=search_res.imageIds
                )
            )
    except grpc.RpcError as e:
        logging.error(f"[METADATA] unavailable: {e}")
        return jsonify({"error": "Metadata unavailable"}), 503

    # protobuf → plain JSON (same as JS)
    images = [
        {
            "id": img.id,
            "name": img.name,
            "tags": list(img.tags),
        }
        for img in meta_res.images
    ]

    return jsonify(images)